# Deploy to Render (Free) - Complete Guide

Render offers 750 free hours per month per service with automatic HTTPS.

## Step 1: Prepare Repository

Ensure your code is on GitHub with proper structure.

## Step 2: Create render.yaml

Create this file in your project root:

```yaml
# render.yaml
services:
  - type: web
    name: heartdisease-api
    env: docker
    dockerfilePath: ./api/Dockerfile
    dockerContext: ./api
    envVars:
      - key: PORT
        value: 8000
    
  - type: web
    name: heartdisease-streamlit
    env: docker
    dockerfilePath: ./streamlit/Dockerfile
    dockerContext: ./streamlit
    envVars:
      - key: PORT
        value: 8501
      - key: API_URL
        fromService:
          type: web
          name: heartdisease-api
          property: host
```

## Step 3: Update Dockerfiles for Render

### Update api/Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY classification_pipeline.py .
COPY db_utils.py .

# Create models directory (will be populated via volume or copy)
RUN mkdir -p /app/models

# Copy models (you'll need to add models to api directory)
COPY models/ ./models/

EXPOSE $PORT

CMD uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Update streamlit/Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Create data directory
RUN mkdir -p /app/data

# Copy data files
COPY data/ ./data/

EXPOSE $PORT

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

## Step 4: Copy Required Files

```bash
# Copy models to api directory
cp -r models/ api/

# Copy data to streamlit directory  
cp -r data/ streamlit/

# Copy db_utils to api directory (already done)
cp db_utils.py api/
```

## Step 5: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will detect `render.yaml` and create both services

## Step 6: Configure Environment Variables

After deployment:
1. Go to your Streamlit service
2. Add environment variable:
   - `API_URL`: `https://your-api-service.onrender.com`

## Free Tier Limitations

- **750 hours/month** per service
- **Services sleep** after 15 minutes of inactivity
- **Cold starts** take 30-60 seconds
- **Custom domains** available on free tier

## Cost: FREE
- Perfect for demos and portfolios
- Automatic HTTPS certificates
- Git-based deployments

## Alternative: Single Service on Render

Create a single `Dockerfile` in project root:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies and supervisor
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 curl supervisor && \
    rm -rf /var/lib/apt/lists/*

# Copy and install API dependencies
COPY api/requirements.txt ./api-requirements.txt
RUN pip install --no-cache-dir -r api-requirements.txt

# Copy and install Streamlit dependencies
COPY streamlit/requirements.txt ./streamlit-requirements.txt
RUN pip install --no-cache-dir -r streamlit-requirements.txt

# Copy application files
COPY api/ ./api/
COPY streamlit/ ./streamlit/
COPY models/ ./models/
COPY data/ ./data/
COPY db_utils.py ./api/

# Create supervisor configuration
RUN echo '[supervisord]\n\
nodaemon=true\n\
\n\
[program:api]\n\
command=uvicorn app:app --host 0.0.0.0 --port 8000\n\
directory=/app/api\n\
autostart=true\n\
autorestart=true\n\
\n\
[program:streamlit]\n\
command=streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
directory=/app/streamlit\n\
environment=API_URL="http://localhost:8000"\n\
autostart=true\n\
autorestart=true' > /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8501

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

Then create a simple `render.yaml`:

```yaml
services:
  - type: web
    name: heartdisease-app
    env: docker
    dockerfilePath: ./Dockerfile
```

This runs both services in one container, using only one free service slot.