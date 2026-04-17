# Security Considerations

- No personally identifiable information (PII) is stored
- No camera, biometric, or sensor data is used
- All write operations require authentication
- Role separation exists between attendee and staff actions
- API keys (e.g. Gemini) are stored server‑side only
- Client applications never access secrets directly

Security is intentionally simple but explicit and responsible.