# SaamaRegulation

## Setup

1. **Create a virtual environment:**
   ```bash
   pyenv install 3.11.13
   pyenv shell 3.11.13
   python3 -m venv venv
   source venv/bin/activate 
   python --version
   ```

2. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `requirements.txt` — Python dependencies
- `api/` — Source code

# 

gcloud auth login
gcloud config set project compliance-os
gcloud services enable run.googleapis.com
 gcloud services enable run.googleapis.com cloudbuild.googleapis.com
 gcloud builds submit --tag gcr.io/compliance-os/saama-regulation
 gcloud run deploy saama-regulation \ 
  --image gcr.io/compliance-os/saama-regulation \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars \
PINECONE_API_KEY=pcs....,\
OPENAI_API_KEY=sk...,\
DATABASE_URL=postgresql://postgres:....,\
COHERE_API_KEY=...
