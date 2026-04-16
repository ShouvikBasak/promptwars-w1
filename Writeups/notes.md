# Physical Event Experience

## Problem Statement

Design a solution that improves the physical event experience for attendees at large-scale sporting venues. The system should address challenges such as crowd movement, waiting times, and real-time coordination, while ensuring a seamless and enjoyable experience.

Your submission consists of two parts:
    Technical: Codebase (GitHub Repo) + Live Preview (Cloud Run URL).
    Narrative: A LinkedIn post of your build to share with the community.

$5 - [PromptWars: W1, Pan India, India - 2026]
Your credit will allow you to use Google Cloud, Gemini API and Firebase.

## Instructions

1. Before You Begin

Make sure the following prerequisites are completed:

    Google Antigravity is downloaded and set up on your system
    Git is installed and configured
    You have an active GitHub account
    You are able to create and manage public repositories

2. Important Rules

    You have a maximum of 2 submission attempts for the Warm Up Round
    You have a maximum of 4 submission attempts (For Actual Challenge Round)
    The repository size must be less than 1 MB
    The GitHub repository must be public
    The repository should contain only one branch
    Failure to follow these rules may result in your submission not being evaluated

3. Challenge Expectations

Your solution should demonstrate:

    Ability to build a smart, dynamic assistant
    Logical decision making based on user context
    Effective use of Google Services
    Practical and real-world usability
    Clean and maintainable code

Participants must choose one of the provided challenge verticals and design their solution around that persona and logic.
4. How to Work on Your Project

    Create a new repository on GitHub
    Ensure the repository is set to public
    Open Google Antigravity
    Clone your repository inside Antigravity
    Build your solution through prompting and coding
    Regularly commit and push your progress
    Keep all work within a single branch

5. What to Submit

Note: For detail guide on how to submit. Please refer to the document
Link

Your submission must include:

    A public GitHub repository link
    Complete project code inside the repository
    A README explaining:
        Your chosen vertical
        Approach and logic
        How the solution works
        Any assumptions made

6. Evaluation Focus Areas

Submissions will be reviewed on:

    Code Quality – structure, readability, maintainability
    Security – safe and responsible implementation
    Efficiency – optimal use of resources
    Testing – validation of functionality
    Accessibility – inclusive and usable design
    Google Services – meaningful integration of Google Services

## IDEATION: Prompt to brainstorm ideas

Initial prompt to Copilot for ideation

I am participating in the Google PromptWars Hackathon, and I need to design a solution that improves the physical event experience for attendees at large-scale sporting venues. The system should address challenges such as crowd movement, waiting times, and real-time coordination, while ensuring a seamless and enjoyable experience. I have $5 credit to use Google Cloud, Gemini API, and Firebase for my project. Can you help me brainstorm some ideas on how to approach this problem?

As a judging criteria, my solution will be evaluated on code quality, security, efficiency, testing, accessibility, and the use of Google services. I want to make sure that my solution is not only innovative but also practical and user-friendly.

The submission will consist of two parts: a technical component, which includes a codebase hosted on GitHub and a live preview hosted on Cloud Run, and a narrative component, which is a LinkedIn post sharing my build with the community.

I have to use Google Antigravity to create the solution.

Can you help me brainstorm some ideas on how to approach this problem and design a solution that meets the criteria mentioned above? Also, what are similar existing websites that perform similar functions, and how can I differentiate my solution from them?

## Planning phase - laying the foundations

Based on the above, have done the following:

- Created a git repo "promptwars-w1" which is private now and will make public once my project is ready for submission
- Cloned the git repo locally and opened using Antigravity
- Created the README.md

What are now the best practices to build the project using Antigravity. Before I actually start building the project I would go step by step setting up the best practices and follow accordingly so that the foundations are strong and the code base meets all the criteria for AI to evaluate the following parameters:
    Code Quality – structure, readability, maintainability
    Security – safe and responsible implementation
    Efficiency – optimal use of resources
    Testing – validation of functionality
    Accessibility – inclusive and usable design
    Google Services – meaningful integration of Google Services

Recommendations:
Think of this as “how a senior engineer would use Antigravity intentionally”, not vibe‑coding.

### Create RULES

### Create CONSTRAINTS

Make Antigravity “auditable” in your repo (this is a differentiator)

They are control surfaces for Antigravity. In Antigravity terms: these are Artifacts the agent can reason against instead of improvising.

/SPECS.md
/ARCHITECTURE.md
/ASSUMPTIONS.md
/SECURITY.md
/ACCESSIBILITY.md
/TESTING.md

## Evaluation Focus

|Focus Area|How this design helps|
|----------|---------------------|
|Code quality|Clear separation: attendee vs ops logic|
|Security|Justifiable role separation (even if simple)|
|Efficiency|Human-in-loop avoids heavy ML / sensors|
|Testing|Easy to unit-test decision logic|
|Accessibility|Ops UI can be keyboard-only|
|Google servicesFirebase Auth + Firestore + Gemini|


## Phase 1 — Scope Lock & Planning (NO CODE)

Goal: Freeze scope and architecture so the agent cannot drift later.

### Prompt 1.1 — Scope Alignment & Risk Check
Mode: Planning / Agent

You are acting as a senior software architect reviewing an AI‑assisted hackathon project.

Read the following files carefully:
- README.md
- ARCHITECTURE.md
- ASSUMPTIONS.md
- ACCESSIBILITY.md
- SECURITY.md
- TESTING.md
- SPEC.md

Your task:
1. Verify that the scope is cohesive and realistic for a demo‑ready MVP.
2. Identify any scope ambiguity or over‑engineering risk.
3. Propose clarifications ONLY if strictly necessary.

Constraints:
- Do NOT generate any code.
- Do NOT suggest new features.
- Keep the response concise (max 20 bullet points).

Output:
Create a markdown artifact named IMPLEMENTATION_SCOPE_REVIEW.md.

#### Actions following the findings from the review:
Update files to include clarifications and reduce ambiguitys. Ask the Agent again to review and provide a findings in v2 of the file.

### Prompt 1.2 — Implementation Plan (Controlled)
Mode: Planning / Agent

Based strictly on:
- README.md
- ARCHITECTURE.md
- ASSUMPTIONS.md
- ACCESSIBILITY.md
- SECURITY.md
- TESTING.md
- SPEC.md
- Implementation_Scope_Review_v2.md

Create a high‑level implementation plan.

Rules:
- Maximum 12 steps.
- Each step must map directly to content in README.md.
- No step may introduce a new capability not already described.
- Absolutely no code generation.

Output:
Create a markdown artifact named IMPLEMENTATION_PLAN.md.


## Phase 2 — Data, API & AI Contracts (Still NO UI)

Goal: Lock interfaces before code so quality + efficiency are automatic.

### Prompt 2.1 — Firestore Data Model
Mode: Agent
Impact: Efficiency, Maintainability, Security

Define the Cloud Firestore data model for this project.

Input:
- README.md
- ARCHITECTURE.md
- ASSUMPTIONS.md
- ACCESSIBILITY.md
- SECURITY.md
- TESTING.md
- SPEC.md
- IMPLEMENTATION_PLAN.md

Rules:
- Use the fewest collections possible.
- Each collection must have a clear purpose.
- No optional fields unless justified.
- Avoid nested subcollections unless necessary.
- Include field names, types, and descriptions.

Output:
Create a markdown artifact named DATA_MODEL.md.

Do NOT generate code.

### Prompt 2.2 — Backend API Contract
Mode: Agent
Impact: This prevents “one more endpoint” creep.

Define the backend API contract for Cloud Run.

Requirements:
- List endpoints with purpose.
- Describe request and response structures.
- Explicitly state validation rules.
- Specify error handling behavior.

Constraints:
- Only endpoints required by README.md.
- No background jobs, no streaming, no webhooks.

Output:
Create a markdown artifact named API_CONTRACT.md.

No code generation.

### Prompt 2.3 — Gemini AI Contract (Extremely Important)
Mode: Agent

This file protects: Cost, Safety, Testability,Judge trust

Define the AI assistant behavior as a strict contract.

Inputs:
- User context (location, nearby POIs)
- Aggregated crowd data
- Optional accessibility preferences

Outputs:
- JSON only
- Fixed schema
- Max 3 recommendation options
- Plain language explanations

Rules:
- No hallucinated facts.
- No external knowledge assumptions.
- No output longer than 120 tokens.
- If confidence is low, assistant must state uncertainty.

Output:
Create a markdown artifact named AI_CONTRACT.md.

Do NOT generate code.

## Phase 3 — Controlled Code Generation (Now Coding Begins)

Rule: One layer at a time. Never mix responsibilities.

### Prompt 3.1 — Backend Skeleton (Cloud Run)
Mode: Agent
Language: Python
GCP Project ID: promptwars-hackathon-493401 

Generate a minimal Cloud Run backend service.

Must comply with:
- API_CONTRACT.md
- AI_CONTRACT.md
- SECURITY.md

Requirements:
- One endpoint: /recommend
- Input validation enforced
- Gemini API called server‑side only
- JSON responses only
- Clear comments explaining logic
- Python programming language

Constraints:
- No features not listed in API_CONTRACT.md
- No frontend code
- No database writes yet

Generate code only.

The generated file is saved as `main.py` in the root directory. This becomes the foundation file.

```
The code has been successfully saved to the repository as main.py. This serves as your minimal, validated FastAPI foundation file, perfectly aligned with the constraints outlind in your API and AI contracts.

Let me know if you would like me to set up a requirements.txt file for it or if you have the next prompt ready!
```

`requirements.txt` generated. Created but not yet installed locally

### Prompt 3.2 — Data Aggregation Logic

Extend the backend to include crowd data aggregation logic.

Rules:
- Must follow DATA_MODEL.md exactly.
- Aggregation must be time‑bounded.
- Include confidence scoring logic.

Constraints:
- Keep logic simple and readable.
- No premature optimizations.

Generate only the related code section and explain briefly.

`aggregation.py` generated and saved in the root directory.


### Prompt 3.3 — Attendee UI (Minimal & Accessible)

Generate the attendee web UI.

Requirements:
- Reads recommendations from /recommend
- Displays wait times clearly
- Keyboard navigable
- No color‑only indicators

Constraints:
- Minimal HTML/CSS/JS
- No images or heavy assets
- Must respect ACCESSIBILITY.md

Generate code only.

`index.html` generated and saved in the root directory.

### Prompt 3.4 — Staff Ops View (Intentional Minimalism)

Generate a minimal staff operations view.

Requirements:
- View current POI status
- Update wait times
- Send short broadcast messages

Constraints:
- No analytics dashboards
- No charts
- Reuse existing styles where possible

Generate code only.

`ops.html` generated and saved in the root directory.

### Prompt 3.5 — Firestore wiring (read path + TTL)

Update main.py to integrate Cloud Firestore following DATA_MODEL.md.

Requirements:
- Initialize Firestore client safely for Cloud Run.
- Implement TTL filtering: ignore any wait-time inputs older than 15 minutes.
- For now, implement read-only behavior (no writes) unless API_CONTRACT.md explicitly includes write endpoints.
- Ensure Gemini is never called with stale data.

Constraints:
- Follow SECURITY.md (no secrets in client).
- Keep code minimal and readable.
- Add clear comments.

Output:
Modify main.py and (if needed) create a small firestore_client.py helper.

`firestore_client.py` generated and saved in the root directory.

### Prompt 3.6 — Auth verification

Implement Firebase Auth token verification in main.py.

Requirements:
- Verify Firebase ID token for any endpoint that modifies data (if such endpoints exist).
- If only /recommend exists, keep it public-read but rate-limit and validate inputs.
- Add a minimal auth utility module (auth.py) if helpful.

Constraints:
- No new features beyond API_CONTRACT.md
- No secrets in frontend
- Keep code minimal

Output:
Modify main.py and add auth.py if needed.

### Prompt 3.7 — Tests

Create minimal automated tests.

Requirements:
- Unit tests for aggregation.py covering:
  - TTL exclusion (15 min)
  - simple time-decay average behavior (as defined in SPEC.md)
  - confidence behavior (simple, deterministic)
- API validation test for /recommend request schema.

Constraints:
- Use pytest
- Keep tests small and readable

Output:
Create tests/ folder and required test files.

### Prompt 3.8 — Wire UI to /recommend

Update index.html to call the backend /recommend endpoint.

Requirements:
- Use the existing manual Zone selection in the UI.
- Display up to 3 recommendations returned by Gemini (AI_CONTRACT.md JSON schema).
- Must meet ACCESSIBILITY.md:
  - keyboard navigable
  - no color-only indicators
  - plain language

Constraints:
- No frameworks or heavy assets
- Keep repo size small

Output:
Modify index.html only.

### Prompt 3.9 — Fix main.py structure + align routes to API_CONTRACT

Fix main.py so it is valid FastAPI code and matches API_CONTRACT.md exactly.

Requirements:
- Ensure all endpoints are defined at module scope (no nested decorators).
- Endpoints must be exactly:
  - POST /api/signals
  - POST /api/broadcasts
  - POST /api/recommendations
- Keep existing Pydantic models but adjust only if needed to match API_CONTRACT.md.
- Add complete implementations (no placeholder bodies).

Constraints:
- Follow SECURITY.md and AI_CONTRACT.md.
- Keep code minimal and readable.
- Do not introduce new endpoints or features.

Output:
Modify main.py only.

### Prompt 3.10 — Create firestore_client.py and implement Firestore I/O
This implements your RAW + Aggregates model in DATA_MODEL.md (pois, wait_signals, broadcasts).

Create firestore_client.py and wire Firestore operations needed by main.py.

Must follow DATA_MODEL.md strictly:
- Collection: pois (aggregated state)
- Collection: wait_signals (raw inputs with expiresAt = createdAt + 15 minutes)
- Collection: broadcasts (with expiresAt)

Requirements:
- Provide a Firestore client `db` usable in Cloud Run.
- Provide helper functions:
  - get_poi(poi_id)
  - update_poi_aggregate(poi_id, fields)
  - create_wait_signal(poi_id, waitMinutes, submitterRole, uid, createdAt, expiresAt)
  - create_broadcast(zone, type, name, message, createdAt, expiresAt)
  - query_pois_by_zone(zone)

Constraints:
- No new collections.
- Keep writes minimal and schema strictly typed.
- No background jobs.

Output:
Create firestore_client.py and modify main.py only if needed for imports.

### Prompt 3.11 — Implement auth.py (Firebase token validation)

Your API_CONTRACT.md requires auth on these endpoints, and your main.py already imports verify_auth_token and verify_staff_token.

Create or complete auth.py to support Firebase Authentication verification for FastAPI.

Requirements:
- Implement:
  - verify_auth_token(): returns uid (string) or raises HTTPException(401)
  - verify_staff_token(): returns uid (string) or raises HTTPException(403/401)
- Use Authorization: Bearer <token> header.
- Keep implementation minimal, production-safe, and readable.
- If full Firebase Admin SDK verification is too heavy, implement a clearly marked stub mode for local dev that is disabled by default and requires an env flag to enable.

Constraints:
- Do not store secrets in code.
- Do not change endpoint contracts.
- Avoid adding heavy dependencies unless necessary.

Output:
Create auth.py and update requirements.txt if required.

### Prompt 3.12 — Finish RAW→Aggregate logic in aggregation.py and use it in /api/signals
Your aggregation.py currently defines WaitSignal and a stubbed function; now you need full logic per your earlier constraints: 15-min window, time decay, staff override priority.

Complete aggregation.py and integrate it into main.py /api/signals flow.

Requirements:
- Implement aggregate_poi_wait_time(signals, current_time) to return:
  - newAggregatedWaitMinutes (int)
  - confidenceScore (float 0..1)
  - isStaffOverride (bool)
- Rules:
  - Only consider signals within last 15 minutes (createdAt cutoff).
  - Use a simple time-decay average (no complex heuristics).
  - If any staff signal exists in the window, it overrides and sets isStaffOverride=true and confidenceScore=1.0.
- main.py /api/signals must:
  - write signal to wait_signals
  - read TTL-window signals for poiId
  - compute aggregate
  - update pois document

Constraints:
- Keep code minimal and testable.
- No background jobs, no extra features.

Output:
Modify aggregation.py and main.py.

### Prompt 3.13 — Implement Gemini call for /api/recommendations (JSON-only enforcement)

Your AI contract is strict: JSON only, max 3 options, max 120 tokens, no hallucinations.

Implement /api/recommendations in main.py following AI_CONTRACT.md.

Requirements:
- Fetch POIs for the provided zone (from Firestore).
- Pass only these fields to Gemini: id, type, currentWaitMinutes, confidenceScore, and the user's accessibilityPreferences.
- Enforce AI output:
  - Must be JSON only
  - Must match fixed schema: {"recommendations": [ ... max 3 ... ]}
  - Must be <= 120 tokens
- If output is not valid JSON or schema mismatch, return 503 with safe error message.

Constraints:
- No external knowledge assumptions.
- No extra endpoints.
- Keep code minimal and readable.

Output:
Modify main.py only.

### Prompt 3.14 — Add minimal tests (fast wins for judging)
This is the minimum that earns real “Testing” points.

Create minimal automated tests using pytest.

Requirements:
- tests/test_aggregation.py:
  - TTL window exclusion
  - time-decay average produces expected value
  - staff override behavior
- tests/test_api_validation.py:
  - /api/signals rejects invalid waitMinutes
  - /api/broadcasts rejects message > 200 chars
  - /api/recommendations rejects nearbyPOIs > 20 (if validated)

Constraints:
- Keep tests small and readable.
- Avoid Firestore dependency in unit tests (mock where needed).

Output:
Create tests/ folder and add test files. Update requirements.txt if needed.

## FIXES as recommended by Copilot after reviewing `main.py` and `aggregation.py`

### Prompt A — Fix [main.py] endpoint structure

Fix main.py so it is valid FastAPI code.

Requirements:
- Ensure all endpoint decorators are defined at module scope (not nested).
- Fully implement these endpoints exactly:
  - POST /api/recommendations
  - POST /api/signals
  - POST /api/broadcasts
- Keep behavior aligned with API_CONTRACT.md and AI_CONTRACT.md.
- Use firestore_client.py helpers for DB reads/writes.

Constraints:
- Do not introduce new endpoints or features.
- Keep code minimal and readable.

Output:
Modify main.py only.

### Prompt B — Fix dependencies in [requirements.txt]  (security + efficiency)

Update requirements.txt to match actual imports and remove unused dependencies.

Context:
- main.py uses fastapi, uvicorn, pydantic, google.generativeai
- firestore_client.py and auth.py use firebase_admin
- firestore access is via firebase_admin.firestore, not google-cloud-firestore directly

Requirements:
- Add missing runtime dependencies required by the current code.
- Remove packages not used by this repo (to reduce attack surface and improve efficiency).

Output:
Modify requirements.txt only.

### Prompt C — Make WaitSignal robust to extra Firestore fields (prevent runtime crash)

Fix aggregation.py so WaitSignal creation does not fail when Firestore documents contain extra fields.

Requirements:
- Keep WaitSignal fields as-is (waitMinutes, submitterRole, createdAt).
- Configure Pydantic so extra keys in the input dict do not raise validation errors.
- Do not add new logic beyond this.

Output:
Modify aggregation.py only.

### Prompt D — Enforce staff role for staff signals (security points)

Harden /api/signals security in main.py.

Requirements:
- If request.submitterRole == "staff", require verify_staff_token.
- If request.submitterRole == "attendee", verify_auth_token is sufficient.
- Keep response and schema unchanged.

Constraints:
- Do not add new endpoints.
- Keep changes minimal and readable.

Output:
Modify main.py only.

### Prompt E — Fix query_pois_by_zone to include POI id

Update firestore_client.py helper query_pois_by_zone so each returned POI includes its document id.

Requirement:
- Return list items like: {"id": doc.id, ...doc.to_dict()}

Output:
Modify firestore_client.py only.

### Prompt F — Add minimal tests
Once the backend starts cleanly locally, add tests (fast wins).

Create minimal automated tests using pytest.

Requirements:
- tests/test_aggregation.py:
  - TTL exclusion (>15 minutes ignored)
  - staff override takes precedence and sets confidenceScore=1.0
  - time-decay average returns an int wait time and confidence in 0..1
- tests/test_api_validation.py:
  - /api/signals rejects waitMinutes <0 or >120
  - /api/broadcasts rejects name >50 or message >200

Constraints:
- Keep tests small and readable.
- Avoid real Firestore calls in unit tests (mock where needed).

Output:
Create tests/ folder and add test files. Update requirements.txt if needed.

### Prompt G — Fail fast on missing GEMINI_API_KEY in non-dev mode

Update main.py to fail fast on startup when GEMINI_API_KEY is missing in non-dev mode.

Current behavior to change:
- genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "STUB_API_KEY"))

Required behavior:
- If GEMINI_API_KEY is missing or empty AND DEV_MODE is not enabled, raise a RuntimeError during startup with a clear message.
- DEV_MODE is enabled only when environment variable DEV_MODE == "true".
- If DEV_MODE == "true", allow missing GEMINI_API_KEY and keep a clearly labeled stub key path for local development only.

Constraints:
- Do not change any API routes, request/response schemas, or business logic.
- Keep code minimal and readable.
- Ensure the error happens at app import/startup time (not inside endpoints).

Output:
Modify main.py only.

## Deployment

You are the deployment engineer. Deploy this existing repository to Google Cloud Run.

Context:
- Google Cloud Project ID: promptwars-hackathon-493401
- Target: Cloud Run (managed)
- App: FastAPI service in main.py
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Requirements file: requirements.txt

Hard requirements:
1) Use gcloud to authenticate if required:
   - gcloud auth login
   - gcloud auth application-default login
   - gcloud config set project promptwars-hackathon-493401
2) Build and deploy to Cloud Run from this repo.
3) Set required environment variables on the Cloud Run service:
   - GEMINI_API_KEY=<ask me to paste the value securely if needed>
   - DEV_MODE=false
   - USE_AUTH_STUB=true  (for demo only)
4) Ensure the deployed service listens on $PORT (Cloud Run requirement).
5) After deployment, verify the service by calling:
   - POST /api/recommendations
6) Produce a Walkthrough artifact that includes:
   - the final Cloud Run service URL
   - the exact gcloud commands executed (or MCP actions)
   - verification result (HTTP status + sample response shape)
   - any changes made to files (if you had to adjust launch command)

Constraints:
- Do not refactor application logic.
- Do not add new features.
- Only make minimal changes required for Cloud Run deployment.
- If any permission prompt appears for terminal or cloud actions, request my approval before proceeding.





























