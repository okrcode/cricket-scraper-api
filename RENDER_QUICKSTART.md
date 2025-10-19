# Render Deployment - Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Install Render CLI

```bash
npm install -g @render-cloud/cli
```

**Don't have Node.js?** Download from [nodejs.org](https://nodejs.org/)

---

### Step 2: Login to Render

```bash
render login
```

This will open your browser for authentication. If you don't have a Render account, sign up at [render.com](https://render.com) (it's free!).

---

### Step 3: Prepare Your Repository

Make sure your code is in a Git repository:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for Render deployment"

# Push to GitHub/GitLab/Bitbucket
git remote add origin <your-repo-url>
git push -u origin main
```

---

### Step 4: Deploy to Render

#### **On Windows:**
```bash
deploy_render.bat
```

#### **On Linux/Mac:**
```bash
chmod +x deploy_render.sh
./deploy_render.sh
```

Or manually:
```bash
render up
```

---

### Step 5: Configure CORS (Important!)

After deployment, set allowed domains:

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your service
3. Go to **Environment** tab
4. Add environment variable:
   - **Key:** `ALLOWED_DOMAINS`
   - **Value:** `https://your-domain.com,https://another-domain.com`
5. Click **Save Changes**

---

## ✅ That's It!

Your API is now live! 

### Access Your API

```
https://cricket-scraper-api.onrender.com
```

### Test Endpoints

```bash
# Health check
curl https://your-app.onrender.com/

# Get all matches
curl https://your-app.onrender.com/matches/all

# Get live odds
curl https://your-app.onrender.com/live/odds
```

---

## 📊 Monitor Your Service

### View Logs
```bash
render logs -f
```

### Check Service Status
```bash
render services list
```

### Open in Browser
```bash
render open
```

---

## 🔧 Common Issues

### Issue: Deployment Failed

**Solution:** Check logs
```bash
render logs --tail 200
```

### Issue: Service Not Starting

**Solutions:**
1. Verify `requirements.txt` has all dependencies
2. Check environment variables are set correctly
3. Review build logs in Render Dashboard

### Issue: "Render CLI not found"

**Solution:** Install Node.js first, then:
```bash
npm install -g @render-cloud/cli
```

---

## 💰 Pricing

- **Free Tier**: Available with limitations (services spin down after inactivity)
- **Starter Plan**: $7/month (always-on service)
- **Pro Plans**: Starting at $15/month

See [Render Pricing](https://render.com/pricing) for details.

---

## 📚 Next Steps

- [Full Deployment Guide](DEPLOYMENT_RENDER.md)
- [Render Documentation](https://render.com/docs)
- [Render CLI Reference](https://render.com/docs/cli)

---

## 🆘 Need Help?

- Check [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md) for detailed instructions
- Visit [Render Community](https://community.render.com)
- Contact [Render Support](https://render.com/support)
