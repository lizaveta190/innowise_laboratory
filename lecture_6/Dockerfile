# Use an official Python image as the base
FROM python:3.11-slim

# Install dependencies
RUN pip install fastapi uvicorn

# Copy application code into the container
COPY main.py .

# Start Uvicorn server to run FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]