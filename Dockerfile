# Use official Python slim image
FROM python:3.11.13-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=True

EXPOSE 8080

CMD ["sh", "-c", "streamlit run main.py --server.port $PORT --server.address 0.0.0.0"]
