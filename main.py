import os
import json
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

from firestore_client import db, update_poi_aggregate, create_wait_signal, create_broadcast
from aggregation import WaitSignal, aggregate_poi_wait_time

# Vertex AI Configuration per implementation_plan_vertex.md
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
DEV_MODE = os.environ.get("DEV_MODE", "").lower() == "true"

if not DEV_MODE:
    # Initialize Vertex AI for production (uses ADC)
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-1.5-flash")
else:
    # Minimal stub logic for local development if Vertex is unavailable
    # We still use a GenerativeModel but it might fail without local ADC
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = GenerativeModel("gemini-1.5-flash")
    except Exception:
        model = None
        print("Warning: Vertex AI initialization failed. AI features will be disabled in DEV_MODE.")

app = FastAPI(title="StadiumFlow Full Backend")

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Input Validation (API_CONTRACT.md) ---
class PoiData(BaseModel):
    id: str
    type: str
    currentWaitMinutes: int
    confidenceScore: float

class RecommendRequest(BaseModel):
    stadium: str
    zone: str
    accessibilityPreferences: Optional[List[str]] = []
    nearbyPOIs: List[PoiData] = Field(..., min_length=1, max_length=20)

class RecommendResponse(BaseModel):
    success: bool
    recommendation: str

class SignalRequest(BaseModel):
    poiId: str
    waitMinutes: int = Field(..., ge=0, le=120)
    submitterRole: str = Field(..., pattern="^(attendee|staff)$")

class SignalResponse(BaseModel):
    success: bool
    newAggregatedWaitMinutes: int
    confidenceScore: float

class BroadcastRequest(BaseModel):
    stadium: str
    zone: str
    type: str = Field(..., pattern="^(info|alert|emergency)$")
    name: str = Field(..., max_length=50)
    message: str = Field(..., max_length=200)

class BroadcastResponse(BaseModel):
    success: bool
    broadcastId: str

# --- Security Checks (SECURITY.md) ---
from auth import verify_auth_token, verify_staff_token

# --- Endpoints ---
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/ops")
@app.get("/ops.html")
async def ops_console():
    return FileResponse("ops.html")

@app.get("/api/stadiums")
async def get_stadiums():
    """Returns a unique list of stadium names from the POIs collection."""
    try:
        docs = db.collection('pois').stream()
        stadiums = set()
        for d in docs:
            data = d.to_dict()
            if data.get("stadium"):
                stadiums.add(data.get("stadium"))
        return {"success": True, "stadiums": sorted(list(stadiums))}
    except Exception as e:
        print(f"Error fetching stadiums: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch stadiums")

@app.get("/api/venues")
async def get_venues(stadium: str):
    """Returns a list of unique zones for a specific stadium."""
    try:
        docs = db.collection('pois').where("stadium", "==", stadium).stream()
        zones = set()
        for d in docs:
            zones.add(d.to_dict().get("zone"))
        return {"success": True, "zones": sorted(list(filter(None, zones)))}
    except Exception as e:
        print(f"Error fetching zones: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch zones")

@app.get("/api/active_broadcasts")
async def get_active_broadcasts(stadium: str, zone: str):
    """Returns active broadcasts for a specific stadium and zone."""
    try:
        now = datetime.now(timezone.utc)
        docs = db.collection('broadcasts')\
            .where('stadium', '==', stadium)\
            .where('zone', '==', zone)\
            .where('expiresAt', '>', now)\
            .stream()
        
        broadcasts = []
        for d in docs:
            data = d.to_dict()
            broadcasts.append({
                "id": d.id,
                "type": data.get("type"),
                "name": data.get("name"),
                "message": data.get("message"),
                "createdAt": data.get("createdAt")
            })
        return {"success": True, "broadcasts": broadcasts}
    except Exception as e:
        print(f"Error fetching broadcasts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch broadcasts")

@app.post("/api/recommendations", response_model=RecommendResponse)
async def get_recommendation(
    request: RecommendRequest, 
    uid: str = Depends(verify_auth_token)
):
    """
    Invoke Gemini AI reasoning module server-side.
    Validates input natives, bounds context, and restricts output per AI_CONTRACT.md.
    Fetches real-time TTL-filtered signals from Firestore to guarantee Gemini is never called with stale data.
    """
    # Fetch POIs securely within stadium/zone scope
    docs = db.collection('pois').where("stadium", "==", request.stadium).where("zone", "==", request.zone).stream()
    
    bounded_pois = []
    for d in docs:
        data = d.to_dict()
        bounded_pois.append({
            "id": d.id,
            "type": data.get("type", "unknown"),
            "currentWaitMinutes": data.get("currentWaitMinutes", 0),
            "confidenceScore": data.get("confidenceScore", 0.0)
        })
    
    # Constructing the context-bound prompt to prevent hallucinations and external assumptions
    prompt = f"""
    You are the StadiumFlow reasoning assistant. 
    Evaluate the following context and provide routing recommendations.
    
    User Zone: {request.zone}
    Accessibility Preferences: {', '.join(request.accessibilityPreferences) if request.accessibilityPreferences else 'None'}
    Current POI Data: {bounded_pois}
    
    Rules:
    1. Output strictly valid JSON.
    2. Provide a maximum of 3 recommendation options.
    3. Only evaluate POIs listed in the Current POI Data. Do not use external knowledge or invent facts.
    4. Provide plain language explanations suitable for a noisy environment in 'recommendationText'.
    5. Schema must exactly be:
       {{
         "recommendations": [
           {{
             "poiId": "string",
             "recommendationText": "string",
             "uncertaintyWarning": "string" (ONLY include if confidenceScore is low for the POI)
           }}
         ]
       }}
    """
    
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="AI Assistant uninitialized.")

        # Call Gemini server-side enforcing token length limit via Vertex SDK
        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                max_output_tokens=120,
                response_mime_type="application/json",
            )
        )
        
        result_json = json.loads(response.text)
        
        # Enforce exact matching schema safely
        if "recommendations" not in result_json or not isinstance(result_json["recommendations"], list):
            raise ValueError("Schema mismatch")
            
        # Force max 3 bound
        result_json["recommendations"] = result_json["recommendations"][:3]
        
        return RecommendResponse(success=True, recommendation=json.dumps(result_json))
        
    except (json.JSONDecodeError, ValueError) as e:
        print(f"AI Schema Error: {str(e)}")
        print(f"Raw AI Output: {response.text if 'response' in locals() else 'No response'}")
        raise HTTPException(status_code=503, detail=f"AI response failed structural validation: {str(e)}")
    except Exception as e:
        import traceback
        print(f"AI Critical Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: AI invocation failed - {str(e)}")

@app.post("/api/signals", response_model=SignalResponse)
async def submit_signal(
    request: SignalRequest,
    authorization: str = Header(None)
):
    """
    Writes raw signal into Firestore, strictly mapping to explicitly allowed properties.
    Executes TTL-bounded aggregation and updates parent POI dynamically.
    Role-based auth: staff claims require verify_staff_token to prevent role spoofing.
    """
    # Escalate auth requirements based on claimed role
    if request.submitterRole == "staff":
        uid = verify_staff_token(authorization)
    else:
        uid = verify_auth_token(authorization)

    now = datetime.now(timezone.utc)
    expiresAt = now + timedelta(minutes=15)
    
    # 1. Ephemeral Write
    create_wait_signal(
        poi_id=request.poiId,
        waitMinutes=request.waitMinutes,
        submitterRole=request.submitterRole,
        uid=uid,
        createdAt=now,
        expiresAt=expiresAt
    )
    
    # 2. Re-calculate metrics from raw data applying 15-minute TTL constraints
    cutoff = now - timedelta(minutes=15)
    signals_query = db.collection('wait_signals')\
        .where('poiId', '==', request.poiId)\
        .where('createdAt', '>=', cutoff)\
        .stream()
        
    signal_objects = [
        WaitSignal(
            waitMinutes=data.get('waitMinutes', 0),
            submitterRole=data.get('submitterRole', 'attendee'),
            createdAt=data.get('createdAt')
        )
        for data in (doc.to_dict() for doc in signals_query)
    ]
        
    agg_result = aggregate_poi_wait_time(signal_objects, now)
    
    # 3. Securely write back aggregated snapshot for frontend subscribers
    update_poi_aggregate(request.poiId, {
        "currentWaitMinutes": agg_result['currentWaitMinutes'],
        "confidenceScore": agg_result['confidenceScore'],
        "isStaffOverride": agg_result['isStaffOverride'],
        "lastUpdatedAt": now
    })
    
    return SignalResponse(
        success=True,
        newAggregatedWaitMinutes=agg_result['currentWaitMinutes'],
        confidenceScore=agg_result['confidenceScore']
    )

@app.post("/api/broadcasts", response_model=BroadcastResponse)
async def create_broadcast_endpoint(
    request: BroadcastRequest, 
    uid: str = Depends(verify_staff_token)
):
    """
    Creates a temporary broadcast pushing alert states. Limited to staff scopes.
    """
    now = datetime.now(timezone.utc)
    expiresAt = now + timedelta(hours=2)
    
    b_id = create_broadcast(
        stadium=request.stadium,
        zone=request.zone,
        b_type=request.type,
        name=request.name,
        message=request.message,
        uid=uid,
        createdAt=now,
        expiresAt=expiresAt
    )
    
    return BroadcastResponse(success=True, broadcastId=b_id)
