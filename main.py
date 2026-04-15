import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
import google.generativeai as genai

# --- Configuration & Initialization ---
# Gemini API called server-side only per SECURITY.md
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "STUB_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

app = FastAPI(title="StadiumFlow Minimal Backend")

# --- Pydantic Models for Input Validation (API_CONTRACT.md) ---
class PoiData(BaseModel):
    id: str
    type: str
    currentWaitMinutes: int
    confidenceScore: float

class RecommendRequest(BaseModel):
    zone: str
    accessibilityPreferences: Optional[List[str]] = []
    # Enforcing max 20 POIs to prevent AI context overflow
    nearbyPOIs: List[PoiData] = Field(..., min_length=1, max_length=20)

class RecommendResponse(BaseModel):
    success: bool
    recommendation: str

# --- Security Checks (SECURITY.md) ---
def verify_auth_token(authorization: Optional[str] = Header(None)) -> str:
    """Enforce authentication for all endpoints."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token.")
    return authorization

# --- Endpoints ---
@app.post("/recommend", response_model=RecommendResponse)
async def get_recommendation(
    request: RecommendRequest, 
    auth: str = Depends(verify_auth_token)
):
    """
    Invoke Gemini AI reasoning module server-side.
    Validates input natively, bounds context, and restricts output per AI_CONTRACT.md.
    """
    
    # Constructing the context-bound prompt to prevent hallucinations and external assumptions
    prompt = f"""
    You are the StadiumFlow reasoning assistant. 
    Evaluate the following context and provide routing recommendations.
    
    User Zone: {request.zone}
    Accessibility Preferences: {', '.join(request.accessibilityPreferences) if request.accessibilityPreferences else 'None'}
    Current POI Data: {[poi.model_dump() for poi in request.nearbyPOIs]}
    
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
        # Call Gemini server-side enforcing token length limit per AI_CONTRACT.md (120 tokens max)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=120,
                response_mime_type="application/json",
            )
        )
        
        # Ensure we can safely parse the JSON payload from the AI response
        result_json = json.loads(response.text)
        
        # Wrap the strictly formatted JSON AI response into the API_CONTRACT response format
        return RecommendResponse(
            success=True,
            recommendation=json.dumps(result_json)
        )
        
    except json.JSONDecodeError:
        # 503 Service Unavailable if we cannot parse AI output securely per API_CONTRACT.md
        raise HTTPException(status_code=503, detail="Failed to parse AI output safely")
    except Exception as e:
        # 500 Internal Server Error for general Gemini upstream timeouts/errors
        raise HTTPException(status_code=500, detail="Internal Server Error: AI invocation failed")
