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

- **GUI Accessibility**: Confirmed the Attendee Hub loads at the root URL with the "StadiumFLOW" premium design.
- **Navigation Flow**: Verified the "Staff Portal" link correctly routes to the `/ops` console and the "Back to Hub" link returns users to the main screen.
- **Content-Type**: Verified all frontend routes return `text/html` headers.

> [!TIP]
> To further test, you can seed POI data into your Firestore `pois` collection in the Google Cloud Console.
