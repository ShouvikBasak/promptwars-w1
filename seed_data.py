import firebase_admin
from firebase_admin import firestore
from datetime import datetime, timezone

def seed():
    # Initialize Firebase if not already
    try:
        firebase_admin.initialize_app()
    except ValueError:
        pass

    db = firestore.client()
    
    # Sample POIs with a 'stadium' field
    pois = [
        # Stadium: Grand Central Arena
        {
            "id": "GCA-R-101",
            "name": "North Gate Restroom",
            "type": "restroom",
            "zone": "North Entrance",
            "stadium": "Grand Central Arena",
            "currentWaitMinutes": 5,
            "confidenceScore": 0.8,
            "isStaffOverride": False,
            "lastUpdatedAt": datetime.now(timezone.utc)
        },
        {
            "id": "GCA-C-201",
            "name": "North Gate Hot Dogs",
            "type": "concession",
            "zone": "North Entrance",
            "stadium": "Grand Central Arena",
            "currentWaitMinutes": 15,
            "confidenceScore": 0.9,
            "isStaffOverride": False,
            "lastUpdatedAt": datetime.now(timezone.utc)
        },
        {
            "id": "GCA-R-202",
            "name": "South Concourse Restroom",
            "type": "restroom",
            "zone": "South Concourse",
            "stadium": "Grand Central Arena",
            "currentWaitMinutes": 10,
            "confidenceScore": 0.7,
            "isStaffOverride": False,
            "lastUpdatedAt": datetime.now(timezone.utc)
        },
        # Stadium: Blue Ribbon Stadium
        {
            "id": "BRS-C-101",
            "name": "East Wing Tacos",
            "type": "concession",
            "zone": "East Wing",
            "stadium": "Blue Ribbon Stadium",
            "currentWaitMinutes": 8,
            "confidenceScore": 0.95,
            "isStaffOverride": False,
            "lastUpdatedAt": datetime.now(timezone.utc)
        },
        {
            "id": "BRS-R-303",
            "name": "Main Level Restroom",
            "type": "restroom",
            "zone": "Main Level",
            "stadium": "Blue Ribbon Stadium",
            "currentWaitMinutes": 12,
            "confidenceScore": 1.0,
            "isStaffOverride": True,
            "lastUpdatedAt": datetime.now(timezone.utc)
        },
        {
            "id": "BRS-E-105",
            "name": "Gate 5 Exit",
            "type": "exit",
            "zone": "Gate 5",
            "stadium": "Blue Ribbon Stadium",
            "currentWaitMinutes": 3,
            "confidenceScore": 0.9,
            "isStaffOverride": False,
            "lastUpdatedAt": datetime.now(timezone.utc)
        }
    ]

    print("Seeding POIs for multi-stadium support...")
    # First, clear existing POIs to avoid mix
    existing_docs = db.collection('pois').stream()
    for d in existing_docs:
        d.reference.delete()
    
    for poi in pois:
        doc_id = poi["id"]
        db.collection('pois').document(doc_id).set(poi)
        print(f"  - Seeded POI: {doc_id} in {poi['stadium']} / {poi['zone']}")

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
