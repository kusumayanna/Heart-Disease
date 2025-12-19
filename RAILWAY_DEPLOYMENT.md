# 🚀 Deploy to Railway - Complete Guide

Your Heart Disease Classification app is now ready for Railway deployment!

## ✅ Pre-deployment Checklist

- [x] Docker images build successfully
- [x] Models and data embedded in containers
- [x] Environment variables configured
- [x] Local testing passed
- [x] Railway-compatible configuration ready

## 🎯 Deployment Options

### Option 1: GitHub Integration (Recommended)

1. **Push to GitHub** (if not already done):
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Deploy via Railway Dashboard**:
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect docker-compose.yml

3. **Configure Services**:
   Railway will create two services:
   - `api` (FastAPI backend)
   - `streamlit` (Frontend)

4. **Set Environment Variables**:
   - Go to Streamlit service → Variables
   - Add: `API_URL` = `https://your-api-service.railway.app`
   - Railway provides the API service URL in the dashboard

### Option 2: Railway CLI

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Deploy**:
```bash
# Run the deployment script
./deploy-railway.sh

# Or manually:
railway login
railway init
railway up
```

## 🔧 Railway Configuration

Your project includes these Railway-ready files:

- `railway.toml` - Railway configuration
- `railway.docker-compose.yml` - Railway-optimized compose file
- Updated Dockerfiles with PORT environment variable support

## 📱 Post-Deployment Steps

1. **Get Service URLs**:
   - Go to Railway dashboard
   - Note your API service URL (e.g., `https://api-production-xxxx.railway.app`)
   - Note your Streamlit URL (e.g., `https://streamlit-production-xxxx.railway.app`)

2. **Update API_URL**:
   - In Railway dashboard → Streamlit service → Variables
   - Set `API_URL` to your API service URL
   - Redeploy Streamlit service

3. **Test Deployment**:
   - Visit your Streamlit URL
   - Try making a prediction
   - Check API docs at `your-api-url/docs`

## 💰 Railway Pricing

**Free Tier**:
- $5 credit monthly
- 500 execution hours
- Perfect for demos and portfolios

**Usage Estimate**:
- Your app: ~$2-3/month if running 24/7
- Free tier covers most educational use

## 🔍 Troubleshooting

### Service Won't Start
```bash
# Check logs in Railway dashboard
# Or via CLI:
railway logs
```

### Streamlit Can't Connect to API
1. Verify API service is running
2. Check API_URL environment variable
3. Ensure API service is publicly accessible

### Build Failures
1. Check Dockerfile syntax
2. Verify all files are committed to git
3. Check Railway build logs

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ Both services show "Active" in Railway dashboard
- ✅ API health check returns 200: `curl your-api-url/health`
- ✅ Streamlit UI loads and can make predictions
- ✅ API docs accessible: `your-api-url/docs`

## 📋 Submission Information

For your course submission, provide:

**Service URLs**:
- Streamlit Frontend: `https://your-streamlit-service.railway.app`
- API Backend: `https://your-api-service.railway.app`
- API Documentation: `https://your-api-service.railway.app/docs`

**Screenshots**:
- Railway dashboard showing both services active
- Streamlit UI with successful prediction
- API documentation page

## 🔄 Updates and Maintenance

**To update your deployment**:
1. Make changes locally
2. Test with `docker-compose up`
3. Commit and push to GitHub
4. Railway auto-deploys from main branch

**To monitor**:
- Railway dashboard shows metrics and logs
- Set up notifications for service issues

## 🆘 Support

If you encounter issues:

1. **Check Railway Status**: [status.railway.app](https://status.railway.app)
2. **Review Logs**: Railway dashboard → Service → Logs
3. **Test Locally**: Ensure `docker-compose up` works
4. **Railway Docs**: [docs.railway.app](https://docs.railway.app)

## 🎯 Next Steps

After successful deployment:

1. **Custom Domain** (optional): Add your own domain in Railway dashboard
2. **Monitoring**: Set up uptime monitoring
3. **Analytics**: Add usage tracking to your Streamlit app
4. **Security**: Consider adding authentication for production use

---

**🎉 Congratulations!** Your Heart Disease Classification app is now live on Railway!

Share your Streamlit URL with others to demonstrate your ML deployment skills.