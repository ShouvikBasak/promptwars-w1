# Architecture Overview

The system follows a simple, layered architecture.

Frontend:
- Lightweight web UI
- Attendee view and minimal staff ops view
- No heavy frameworks or assets

Backend:
- Google Cloud Run service
- Exposes a minimal REST API
- Performs validation, aggregation, and AI calls

Data:
- Cloud Firestore for realtime state
- Small number of flat collections
- No joins or complex relationships

AI:
- Gemini API
- Invoked server‑side only
- Constrained via a strict input/output contract

Non‑goals:
- Background workers
- Streaming pipelines
- Event‑driven orchestration
