# Implementation Scope Review: StadiumFlow

As requested, here is a review of the StadiumFlow hackathon project scope based on the provided documentation.

## 1. Cohesion & MVP Realism
*   **Strong Boundaries:** The explicit exclusion of hardware sensors, background workers, and streaming pipelines keeps the architectural footprint realistically achievable for a hackathon.
*   **Sensible Architecture:** Relying on Firebase/Firestore for real-time state and Cloud Run for the logic provides a stable, modern stack without unnecessary overhead.
*   **Appropriate AI Usage:** Using Gemini solely for server-side reasoning over a constrained data context minimizes hallucination risks and simplifies prompt engineering.
*   **Clear Role Definitions:** The "human-in-the-loop" staff console properly addresses data accuracy without requiring complex machine learning verification.

## 2. Ambiguity & Over-Engineering Risks
*   **Over-Engineering Risk (Confidence Scoring):** The `ARCHITECTURE.md` and `README.md` mention "aggregation and confidence logic." There is a high risk of over-engineering this into a complex heuristic.
*   **Ambiguity Risk (Context Acquisition):** `README.md` states the AI evaluates "User context (location, nearby POIs)." Relying on precise native GPS indoors for a web MVP is notoriously unreliable and difficult to simulate during a demo.
*   **Scale/Cost Risk (Real-time sync):** Excessive frequent writes from thousands of users attempting to send "one-tap wait estimates" could trigger rate limits or quota issues on a free-tier Firestore database.
*   **Ambiguity Risk (Data Lifecycle):** There is no mention of how long wait-time data is retained. Stale data could corrupt the Gemini reasoning module over the course of a demo.

## 3. Proposed Clarifications
*   **Clarification on Location Input:** Explicitly define location context as a manual user selection (e.g., selecting "Zone A" from a dropdown) rather than relying on automated device GPS.
*   **Clarification on Logic Complexity:** Define the confidence algorithm in `SPEC.md` strictly as a simple time-decay average to enforce simplicity.
*   **Clarification on Data Pruning:** Add a constraint to `ARCHITECTURE.md` dictating a short "Time-To-Live" (TTL) strategy (e.g., 15 minutes) for wait-time inputs to ensure the AI always reasons over fresh data.
