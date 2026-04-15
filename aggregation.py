from datetime import datetime, timezone
from typing import List, Dict, Union
from pydantic import BaseModel

# Input model based strictly on DATA_MODEL.md wait_signals
class WaitSignal(BaseModel):
    model_config = {"extra": "ignore"}

    waitMinutes: int
    submitterRole: str  # 'attendee' or 'staff'
    createdAt: datetime

def aggregate_poi_wait_time(signals: List[WaitSignal], current_time: datetime = None) -> Dict[str, Union[int, float, bool]]:
    """
    Evaluates raw wait signals to produce an aggregated wait time and confidence score.
    Follows strict 15-minute time-bounding and applies Staff override priority.
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
        
    valid_signals = []
    
    # 1. strictly drop any inputs older than 15 minutes (fallback for Firestore TTL)
    for sig in signals:
        age_minutes = (current_time - sig.createdAt).total_seconds() / 60.0
        if 0 <= age_minutes <= 15:
            valid_signals.append((sig, age_minutes))
            
    if not valid_signals:
        return {
            "currentWaitMinutes": 0,
            "confidenceScore": 0.0,
            "isStaffOverride": False
        }
        
    # 2. Staff Validation Override (from SPEC.md)
    # If any valid staff signal exists, immediately trust the most recent one.
    staff_signals = [sig for sig, age in valid_signals if sig.submitterRole == 'staff']
    if staff_signals:
        latest_staff_signal = max(staff_signals, key=lambda s: s.createdAt)
        return {
            "currentWaitMinutes": latest_staff_signal.waitMinutes,
            "confidenceScore": 1.0, # Complete certainty due to staff validation
            "isStaffOverride": True
        }
        
    # 3. Time-Decay Average for normal attendee signals
    total_weighted_wait = 0.0
    total_weight = 0.0
    
    for sig, age_minutes in valid_signals:
        # Weight linearly decays from 1.0 (brand new) down to almost 0 as it nears 15 mins
        weight = max(0.1, 1.0 - (age_minutes / 15.0))
        total_weighted_wait += sig.waitMinutes * weight
        total_weight += weight
        
    # 4. Simple Confidence Score Logic
    # Calculates trust based on volume and freshness. A total weight of 3.0 or higher is 100% confidence.
    confidence_score = min(1.0, total_weight / 3.0)
    
    return {
        "currentWaitMinutes": round(total_weighted_wait / total_weight),
        "confidenceScore": round(confidence_score, 2),
        "isStaffOverride": False
    }
