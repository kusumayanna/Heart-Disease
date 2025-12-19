# Deploy to Railway (Free) - 5 Minute Setup

Railway is the easiest way to deploy your Docker app for free.

## Step 1: Prepare Your Repository

1. Push your code to GitHub (if not already done)
2. Ensure your `docker-compose.yml` is in the root directory

## Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your heart disease repo
5. Railway will automatically detect docker-compose.yml

## Step 3: Configure Services

Railway will create two services automatically:
- `api` (FastAPI backend)
- `streamlit` (Frontend)

### Configure API Service:
- **Port**: 8000
- **Environment Variables**: None needed
- **Domain**: Railway provides a free subdomain

### Configure Streamlit Service:
- **Port**: 8501
- **Environment Variables**:
  - `API_URL`: Use the API service's Railway URL
- **Domain**: Railway provides a free subdomain

## Step 4: Update API_URL

After deployment, update the Streamlit service environment:
1. Go to Streamlit service → Variables
2. Set `API_URL` to your API service URL (e.g., `https://your-api-service.railway.app`)
3. Redeploy

## Step 5: Access Your App

- **Streamlit UI**: `https://your-streamlit-service.railway.app`
- **API Docs**: `https://your-api-service.railway.app/docs`

## Cost: FREE
- 500 execution hours/month
- $5 credit monthly
- Perfect for demos and portfolios

## Alternative: Single Service Deployment

If you want to deploy as a single service, create this `Dockerfile`:

```dockerfile
# Multi-stage build for both services
FROM python:3.12-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# API Stage
FROM base as api
WORKDIR /app/api
COPY api/requirements.txt .
RUN pip install -r requirements.txt
COPY api/ .
COPY db_utils.py .

# Streamlit Stage  
FROM base as streamlit
WORKDIR /app/streamlit
COPY streamlit/requirements.txt .
RUN pip install -r requirements.txt
COPY streamlit/ .

# Final stage
FROM base
WORKDIR /app

# Copy both applications
COPY --from=api /app/api ./api
COPY --from=streamlit /app/streamlit ./streamlit
COPY models/ ./models/
COPY data/ ./data/

# Install supervisor to run both services
RUN pip install supervisor

# Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8501

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

And `supervisord.conf`:
```ini
[supervisord]
nodaemon=true

[program:api]
command=uvicorn app:app --host 0.0.0.0 --port 8000
directory=/app/api
autostart=true
autorestart=true

[program:streamlit]
command=streamlit run app.py --server.port=8501 --server.address=0.0.0.0
directory=/app/streamlit
environment=API_URL="http://localhost:8000"
autostart=true
autorestart=true
```

This runs both services in a single container on Railway's free tier.