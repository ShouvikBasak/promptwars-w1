# Project Specification – StadiumFlow

StadiumFlow is a smart, real‑time assistant for improving the in‑venue experience at large sporting events.

The system focuses on:
- reducing congestion
- minimizing waiting times
- improving attendee decision‑making
- enabling lightweight staff coordination

The solution is designed as a **demo‑ready MVP**, not a full production platform.

In scope:
- Attendee recommendations based on real‑time context
- Approximate wait‑time visibility
- Human‑in‑the‑loop staff confirmation
- AI‑assisted reasoning using Gemini

Out of scope:
- Camera or sensor integrations
- Predictive crowd modeling
- Ticketing, payments, or identity systems
- Advanced analytics dashboards

### Confidence and Aggregation Logic

Wait‑time confidence is intentionally defined as a **simple time‑decay average**.

Rules:
- Newer inputs carry higher weight than older inputs
- No complex heuristics, machine learning, or multi‑factor scoring
- Staff confirmation always overrides automated confidence values

This constraint is intentional to maintain clarity, reliability, and implementation simplicity.

### Location Context

User location is captured via **explicit manual selection** (e.g., choosing a Venue Zone or Area)
rather than relying on device GPS.

This approach avoids indoor location inaccuracies and ensures predictable demo behavior.
