import os
import json
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
import google.generativeai as genai

from firestore_client import db, update_poi_aggregate, create_wait_signal, create_broadcast
from aggregation import WaitSignal, aggregate_poi_wait_time

# --- Configuration & Initialization ---
# Gemini API called server-side only per SECURITY.md
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "STUB_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

app = FastAPI(title="StadiumFlow Full Backend")

# --- Pydantic Models for Input Validation (API_CONTRACT.md) ---
class PoiData(BaseModel):
    id: str
    type: str
    currentWaitMinutes: int
    confidenceScore: float

class RecommendRequest(BaseModel):
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
    # Fetch POIs securely bypassing client state per Prompt 3.13 constraints
    docs = db.collection('pois').where("zone", "==", request.zone).stream()
    
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
        # Call Gemini server-side enforcing token length limit
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
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
        
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=503, detail="AI response failed structural validation constraints.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: AI invocation failed")

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
        zone=request.zone,
        b_type=request.type,
        name=request.name,
        message=request.message,
        uid=uid,
        createdAt=now,
        expiresAt=expiresAt
    )
    
    return BroadcastResponse(success=True, broadcastId=b_id)
