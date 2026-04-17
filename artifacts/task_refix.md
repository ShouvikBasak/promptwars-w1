# Task: Final Resolution of StadiumFlow Issues

## Data Seeding
- [x] Update `seed_data.py` with multiple stadiums and zones
- [x] Run `seed_data.py` (Cloud project)

## Backend Refactoring
- [x] Implement `GET /api/stadiums` in `main.py`
- [x] Update `GET /api/venues` to support `stadium` filtering
- [x] Update `GET /api/active_broadcasts` to support `stadium` filtering
- [x] Update `POST /api/broadcasts` to include `stadium` field

## Frontend Implementation
- [x] Update `index.html` with Stadium -> Zone selection
- [x] Update `ops.html` with Stadium selection for overrides and broadcasts
- [x] Verify Broadcast Ticker refreshes correctly

## Deployment & Verification
- [x] Re-deploy to Cloud Run with `USE_AUTH_STUB=true` and `DEV_MODE=true`
- [x] Verify 401 Unauthorized errors are resolved
- [x] Verify dynamic loading of Stadiums and Zones
- [x] Verify live Broadcast Ticker
