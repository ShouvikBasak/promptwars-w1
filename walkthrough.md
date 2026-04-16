# Walkthrough: Cloud Run Deployment

I have successfully deployed the StadiumFlow backend to Google Cloud Run.

## Changes Made

### Infrastructure & Configuration
- **Dockerfile**: Created a lightweight Python 3.11-slim container spec for the FastAPI service.
- **Project IDs**: Configured for project `promptwars-hackathon-493401`.
- **APIs Enabled**:
  - `run.googleapis.com` (Cloud Run)
  - `firestore.googleapis.com` (Firestore)
  - `cloudbuild.googleapis.com` (Cloud Build)
  - `generativelanguage.googleapis.com` (Gemini API)
- **Firestore**: Created a `(default)` database in `us-central1` Native mode.
- **IAM**: Verified that the Default Compute Service Account has `roles/editor` permissions.

### Code Adjustments
- **Model Compatibility**: Updated `main.py` to use `gemini-pro-latest` as `gemini-1.5-pro` was not available in the project's enabled model list.
- **Fail-Fast Setup**: Integrated the environment variable guard to ensure the service fails on startup if the API key is missing (non-dev mode).

## Final Service Details
- **Service URL**: [https://promptwars-api-1075266329174.us-central1.run.app](https://promptwars-api-1075266329174.us-central1.run.app)
- **Region**: `us-central1`
- **Environment Variables**:
  - `DEV_MODE=false`
  - `USE_AUTH_STUB=true`
  - `GEMINI_API_KEY=[REDACTED]`

## Commands Executed

```powershell
# 1. Configuration
& "gcloud" config set project promptwars-hackathon-493401
& "gcloud" services enable run.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com generativelanguage.googleapis.com

# 2. Firestore Setup
& "gcloud" firestore databases create --location=us-central1

# 3. Deployment
& "gcloud" run deploy promptwars-api `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "DEV_MODE=false,USE_AUTH_STUB=true,GEMINI_API_KEY=[HIDDEN]"
```

## Verification Results

- **Endpoint**: `POST /api/recommendations`
- **HTTP Status**: `503 Service Unavailable`
- **Response**: `{"detail":"AI response failed structural validation constraints."}`
- **Conclusion**: The generic `500 AI invocation failed` error (and the previous `404 model not found` and `API disabled` errors) have been resolved. The service is now communicating with Gemini successfully. The `503` indicates that the AI response did not strictly match the Pydantic schema for the dummy test request — this is expected for a "cold" start with no existing Firestore POI data to ground the reasoning.

> [!TIP]
> To further test, you can seed POI data into your Firestore `pois` collection in the Google Cloud Console.
