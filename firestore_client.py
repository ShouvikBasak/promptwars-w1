import os

# Lazy-initialize Firestore to avoid import-time crashes in test environments
_db = None

def _get_db():
    """
    Returns a Firestore client, initializing Firebase on first call.
    Uses Application Default Credentials (ADC) per SECURITY.md — no secrets in code.
    """
    global _db
    if _db is not None:
        return _db

    import firebase_admin
    from firebase_admin import firestore

    try:
        firebase_admin.initialize_app()
    except ValueError:
        # App already initialized (e.g. hot-reload)
        pass

    _db = firestore.client()
    return _db

# Public property — compatible with existing `from firestore_client import db` usage
class _DbProxy:
    """Proxy that defers Firestore init until first attribute access."""
    def __getattr__(self, name):
        return getattr(_get_db(), name)

db = _DbProxy()

# --- Helper functions strictly mapping to DATA_MODEL.md collections ---

def get_poi(poi_id: str) -> dict:
    """Read a single POI document by ID."""
    doc = db.collection('pois').document(poi_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_poi_aggregate(poi_id: str, fields: dict):
    """Merge updated aggregation fields into the POI document."""
    db.collection('pois').document(poi_id).set(fields, merge=True)

def create_wait_signal(poi_id: str, waitMinutes: int, submitterRole: str, uid: str, createdAt, expiresAt):
    """Write a single ephemeral wait signal into the wait_signals collection."""
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

def create_broadcast(stadium: str, zone: str, b_type: str, name: str, message: str, uid: str, createdAt, expiresAt) -> str:
    """Write a broadcast document and return its auto-generated ID."""
    _, doc_ref = db.collection('broadcasts').add({
        "stadium": stadium,
        "zone": zone,
        "type": b_type,
        "name": name,
        "message": message,
        "createdByUid": uid,
        "createdAt": createdAt,
        "expiresAt": expiresAt
    })
    return doc_ref.id

def query_pois_by_zone(zone: str, stadium: str = None) -> list:
    """Return all POI documents matching a specific zone and stadium."""
    query = db.collection('pois').where("zone", "==", zone)
    if stadium:
        query = query.where("stadium", "==", stadium)
    docs = query.stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]
