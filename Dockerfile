FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Start the application using uvicorn
# Cloud Run sets the PORT env var, which we use here
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
