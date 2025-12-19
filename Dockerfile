# Multi-service Dockerfile for Railway deployment
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
COPY db_utils.py ./api/

# Create supervisor configuration
RUN echo '[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:api]\n\
command=uvicorn app:app --host 0.0.0.0 --port 8000\n\
directory=/app/api\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
\n\
[program:streamlit]\n\
command=streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
directory=/app/streamlit\n\
environment=API_URL="http://localhost:8000"\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0' > /etc/supervisor/conf.d/supervisord.conf

# Expose Streamlit port (Railway will map this)
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start supervisor to run both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]