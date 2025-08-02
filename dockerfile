# Use official Python slim image
FROM python:3.13-slim

# Install required system packages
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=True

# Expose port for Flask/Gunicorn
EXPOSE 8080

# Use Gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "api.main:app"]
