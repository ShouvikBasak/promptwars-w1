# Implementation Plan – Cloud Run Deployment

Deploy the StadiumFlow backend to Google Cloud Run with IAM-based authentication.

## Proposed Changes
- [NEW] .gcloudignore
- [MODIFY] IAM: Grant `aiplatform.user` and `datastore.user` to the service account.
