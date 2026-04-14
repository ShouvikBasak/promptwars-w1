# Architecture Overview

The system follows a simple, layered architecture.

Frontend:
- Lightweight web UI
- Attendee view and minimal staff ops view
- No heavy frameworks or assets
- Location awareness is handled through manual zone selection in the UI.
- No automated geolocation services are used.

Backend:
- Google Cloud Run service
- Exposes a minimal REST API
- Performs validation, aggregation, and AI calls

Data:
- Cloud Firestore for realtime state
- Small number of flat collections
- No joins or complex relationships
- Firestore writes are intentionally rate‑limited.
    Constraints:
        - Attendee inputs are aggregated server‑side
        - Client‑side writes are limited to prevent excessive update frequency
        - Real‑time listeners subscribe only to aggregated documents, not raw inputs

AI:
- Gemini API
- Invoked server‑side only
- Constrained via a strict input/output contract

Non‑goals:
- Background workers
- Streaming pipelines
- Event‑driven orchestration


### Data Lifecycle Management

All wait‑time inputs expire after a short Time‑To‑Live (TTL).

Rules:
- Default TTL: 15 minutes
- Expired data is excluded from aggregation and AI reasoning
- Gemini is never invoked with stale or expired inputs
