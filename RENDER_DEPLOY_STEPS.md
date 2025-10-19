# 🚀 Deploy to Render - Complete Guide

## ✅ Prerequisites Completed

- ✓ Node.js installed
- ✓ Git installed and repository initialized  
- ✓ Project files committed to Git
- ✓ `render.yaml` configuration ready

---

## 📋 Deployment Steps

### **Step 1: Create a GitHub Repository**

1. Go to [GitHub](https://github.com) and sign in (or create an account)
2. Click the **"+" icon** → **"New repository"**
3. Repository settings:
   - **Name**: `cricket-scraper-api` (or any name you prefer)
   - **Visibility**: Public or Private (both work with Render)
   - **DO NOT** initialize with README, .gitignore, or license
4. Click **"Create repository"**

### **Step 2: Push Your Code to GitHub**

Copy and run these commands in your terminal:

```powershell
cd "c:\Users\DELL\Desktop\New folder\task\cricket_scraper\cricket_scraper"
$env:Path = "C:\Program Files\Git\cmd;" + $env:Path

# Add your GitHub repository URL (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/cricket-scraper-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username!

If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a [Personal Access Token](https://github.com/settings/tokens) (not your password)

### **Step 3: Deploy to Render**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Sign in or create a free account
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub account if not already connected
5. Select your repository: **`cricket-scraper-api`**
6. Click **"Apply"**

Render will automatically:
- Read your [`render.yaml`](file://c:\Users\DELL\Desktop\New%20folder\task\cricket_scraper\cricket_scraper\render.yaml) configuration
- Create the web service
- Set up environment variables
- Deploy your application

### **Step 4: Configure CORS (Important!)**

After deployment completes:

1. Go to your service in the Render Dashboard
2. Navigate to the **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `ALLOWED_DOMAINS`
   - **Value**: `https://your-frontend-domain.com,https://another-domain.com`
5. Click **"Save Changes"**
6. Your service will automatically redeploy

---

## 🎉 Deployment Complete!

Your API will be available at:
```
https://cricket-scraper-api.onrender.com
```

### Test Your Endpoints

```bash
# Health check
curl https://your-app.onrender.com/

# Get all matches
curl https://your-app.onrender.com/matches/all

# Get live odds
curl https://your-app.onrender.com/live/odds
```

---

## 🔄 Update Your Deployment

To deploy updates:

```powershell
cd "c:\Users\DELL\Desktop\New folder\task\cricket_scraper\cricket_scraper"
$env:Path = "C:\Program Files\Git\cmd;" + $env:Path

# Make your code changes, then:
git add .
git commit -m "Description of your changes"
git push origin main
```

Render will automatically detect the push and redeploy your application!

---

## 📊 Monitor Your Application

- **View Logs**: Dashboard → Your Service → Logs tab
- **Check Metrics**: Dashboard → Your Service → Metrics tab
- **View Events**: Dashboard → Your Service → Events tab

---

## ⚠️ Important Notes

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds (cold start)
- 750 hours/month of runtime (sufficient for one always-on service)

### Upgrade to Paid Plan
For production use:
- **Starter Plan**: $7/month - Always-on, no cold starts
- **Standard Plan**: $25/month - Increased resources

---

## 🛠️ Troubleshooting

### Build Fails
- Check logs in Render Dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `render.yaml` syntax is correct

### Service Won't Start
- Check that PORT environment variable is used correctly
- Verify Gunicorn command in `render.yaml`
- Review application logs for errors

### Data Not Persisting
- Verify disk mount path in `render.yaml`
- Check that application writes to `/opt/render/project/src/app/data`

---

## 📱 Alternative: Deploy via Render Dashboard (Without GitHub)

If you don't want to use GitHub:

1. Create a `.zip` file of your project
2. Go to Render Dashboard
3. Create a **Web Service**
4. Choose **"Deploy from Git"** and connect to a Git provider
5. **OR** use Render's Docker deployment option

---

## 📚 Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [Render Documentation](https://render.com/docs)
- [Python on Render Guide](https://render.com/docs/deploy-fastapi)
- [Render Blueprint Spec](https://render.com/docs/blueprint-spec)
- [Environment Variables](https://render.com/docs/environment-variables)

---

## 🆘 Need Help?

- Check [Full Deployment Guide](DEPLOYMENT_RENDER.md)
- Visit [Render Community](https://community.render.com)
- Contact [Render Support](https://render.com/support)

---

**Ready to deploy? Follow Step 1 above!** 🚀
