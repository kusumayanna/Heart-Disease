#!/bin/bash

echo "🚀 Preparing for Railway deployment..."

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    echo "or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

echo "✅ Railway CLI found"

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway:"
    railway login
fi

echo "✅ Railway authentication successful"

# Create new project or link existing
echo "🔗 Setting up Railway project..."
if [ ! -f "railway.toml" ]; then
    railway init
else
    echo "Railway project already configured"
fi

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "📱 Next steps:"
echo "1. Go to https://railway.app/dashboard"
echo "2. Find your project and services"
echo "3. Configure environment variables if needed"
echo "4. Get your service URLs"
echo ""
echo "🔧 Don't forget to:"
echo "- Set API_URL in Streamlit service to your API service URL"
echo "- Both services should be publicly accessible"