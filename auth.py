import os
from fastapi import Header, HTTPException
import firebase_admin
from firebase_admin import auth

def verify_auth_token(authorization: str = Header(None)) -> str:
    """
    Verify Firebase ID token securely via Firebase Admin SDK per SECURITY.md limits.
    Returns the deeply authenticated user UID.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token format.")
        
    id_token = authorization.split("Bearer ")[1]
    
    # Clearly marked stub mode for local dev/testing
    if os.environ.get("USE_AUTH_STUB") == "true":
        return "stub_verified_uid"
        
    try:
        # Strictly verify cryptographic signature using Application Default Credentials
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token.get('uid')
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized: Token expired.")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Firebase ID token.")

def verify_staff_token(authorization: str = Header(None)) -> str:
    """
    Verify Firebase ID token AND enforce custom 'staff' claims
    per API_CONTRACT.md restrictions for broadcast functionality.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token format.")
        
    id_token = authorization.split("Bearer ")[1]
    
    # Clearly marked stub mode for local dev/testing
    if os.environ.get("USE_AUTH_STUB") == "true":
        # Simulate a token with the staff claim
        return "stub_staff_uid"
        
    try:
        decoded_token = auth.verify_id_token(id_token)
        
        # Enforce explicitly assigned roles mapped in our API_CONTRACT.md
        if decoded_token.get('role') != 'staff':
            raise HTTPException(status_code=403, detail="Forbidden: Action restricted to staff members.")
            
        return decoded_token.get('uid')
    except HTTPException:
        raise # Reraise the 403 Forbidden safely
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized: Token expired.")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Firebase ID token.")
