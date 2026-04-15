import firebase_admin
from firebase_admin import firestore

# Initialize using Application Default Credentials (ADC)
try:
    firebase_admin.initialize_app()
except ValueError:
    pass

# Export the db instance for backend consumption directly if needed
db = firestore.client()

def get_poi(poi_id: str) -> dict:
    doc = db.collection('pois').document(poi_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_poi_aggregate(poi_id: str, fields: dict):
    db.collection('pois').document(poi_id).set(fields, merge=True)

def create_wait_signal(poi_id: str, waitMinutes: int, submitterRole: str, uid: str, createdAt, expiresAt):
    db.collection('wait_signals').add({
        "poiId": poi_id,
        "waitMinutes": waitMinutes,
        "submitterRole": submitterRole,
        "createdByUid": uid,
        "createdAt": createdAt,
        "expiresAt": expiresAt,
        "type": "standard",
        "name": "POI"
    })

def create_broadcast(zone: str, b_type: str, name: str, message: str, uid: str, createdAt, expiresAt) -> str:
    _, doc_ref = db.collection('broadcasts').add({
        "zone": zone,
        "type": b_type,
        "name": name,
        "message": message,
        "createdByUid": uid,
        "createdAt": createdAt,
        "expiresAt": expiresAt
    })
    return doc_ref.id

def query_pois_by_zone(zone: str) -> list:
    docs = db.collection('pois').where("zone", "==", zone).stream()
    return [d.to_dict() for d in docs]
