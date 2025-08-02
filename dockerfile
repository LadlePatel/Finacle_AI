# Use official Python slim image
FROM python:3.13-slim

# (Optional) Install required system packages
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=True

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:${PORT:-8080}", "main:main"]
