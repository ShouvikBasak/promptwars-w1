# Backend API Contract

This document outlines the strict REST API contract for the Google Cloud Run backend. Per the architectural constraints, this API strictly handles writes, aggregation logic, and AI reasoning. Client-side reads (real-time sync) are assumed to directly hit Cloud Firestore via client SDKs. Background workers, webhooks, and streaming are explicitly excluded.

---

## 1. `POST /api/signals`

**Purpose:** 
Accept real-time wait-time inputs from attendees or venue staff. The backend validates the signal, creates a record in the `wait_signals` collection, and synchronously computes/updates the aggregated wait time and confidence score on the parent `pois` document.

**Request Structure:**
```json
{
  "poiId": "string (UUID)",
  "waitMinutes": "number (Integer)",
  "submitterRole": "string ('attendee' | 'staff')"
}
```

**Response Structure:**
```json
{
  "success": "boolean",
  "newAggregatedWaitMinutes": "number",
  "confidenceScore": "number"
}
```

**Explicit Validation Rules:**
- **Authentication:** Request must include a valid Firebase Auth token.
- **Constraints:**
  - `poiId` must map to an existing document in the `pois` collection.
  - `waitMinutes` must be a non-negative integer (e.g., between `0` and `120`).
  - `submitterRole` must be matching the role claim provided inside the Auth token.
- **Rate-Limiting:** UID is extracted from the token; a limit of X requests per rolling minute is enforced.

**Error Handling Behavior:**
- `400 Bad Request`: Validation failure (e.g., `waitMinutes` is negative or missing fields).
- `401 Unauthorized`: Request missing Auth token or token is invalid.
- `403 Forbidden`: Token does not contain the permissions claimed in `submitterRole` (e.g., trying to submit as staff).
- `404 Not Found`: `poiId` does not reference a valid POI.
- `429 Too Many Requests`: User (UID) rate limit exceeded.

---

## 2. `POST /api/broadcasts`

**Purpose:** 
Enable operations staff to push short, localized announcements to attendees within a specific venue zone.

**Request Structure:**
```json
{
  "zone": "string",
  "type": "string ('info' | 'alert' | 'emergency')",
  "name": "string (Short Title)",
  "message": "string"
}
```

**Response Structure:**
```json
{
  "success": "boolean",
  "broadcastId": "string"
}
```

**Explicit Validation Rules:**
- **Authentication:** Must include Auth token representing a `staff` user.
- **Constraints:**
  - `zone` must be a valid non-empty string targeting an existing location grouping.
  - `type` must match one of the predefined accessibility/rendering formats (`info`, `alert`, `emergency`).
  - `name` (Headline) must be strictly under 50 characters.
  - `message` must be under 200 characters to enforce the "short, localized" constraint.

**Error Handling Behavior:**
- `400 Bad Request`: Body fails schema constraints (e.g., message too long, invalid type).
- `401 Unauthorized`: Missing or invalid Auth token.
- `403 Forbidden`: User attempts operation without the `staff` role claim.

---

## 3. `POST /api/recommendations`

**Purpose:** 
Invoke the Gemini AI reasoning module server-side to generate a dynamic, explainable recommendation based on live venue context.

**Request Structure:**
```json
{
  "zone": "string",
  "accessibilityPreferences": ["string"],
  "nearbyPOIs": [
    {
      "id": "string",
      "type": "string",
      "currentWaitMinutes": "number",
      "confidenceScore": "number"
    }
  ]
}
```

**Response Structure:**
```json
{
  "success": "boolean",
  "recommendation": "string"
}
```

**Explicit Validation Rules:**
- **Authentication:** Standard Auth token required.
- **Constraints:**
  - `zone` is mandatory.
  - `nearbyPOIs` array must contain between 1 and 20 items (to prevent AI context overflow).
  - Keys used for AI generation must not leak PII in transit.

**Error Handling Behavior:**
- `400 Bad Request`: Payload exceeds size limits or lacks required fields.
- `401 Unauthorized`: Missing or invalid Auth token.
- `500 Internal Server Error`: Gemini API invocation timed out or encountered an upstream failure.
- `503 Service Unavailable`: Failed to parse or render Gemini reasoning output safely.
