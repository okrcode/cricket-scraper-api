# Render Deployment Guide

This guide explains how to deploy the Cricket Scraper API to Render using the Render CLI.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)
3. **Render CLI**: Install the Render command-line tool

## Deployment Methods

Render supports multiple deployment methods:

1. **Web Dashboard** (Recommended - Easiest)
2. **GitHub/GitLab Integration** (Automatic deployments)
3. **Blueprint (render.yaml)** (Infrastructure as Code)
4. **Render API** (For advanced automation)

**Note:** Render does not have a traditional CLI tool like `@render-cloud/cli`. The easiest way to deploy is through the web dashboard or GitHub integration.

## Setup

### 1. Login to Render
```bash
render login
```
This will open a browser window for authentication.

### 2. Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
```

### 3. Push to Remote Repository
```bash
# Add your remote repository
git remote add origin <your-git-repo-url>
git push -u origin main
```

## Deployment

### Option 1: Using Deployment Script (Recommended)

#### On Windows:
```bash
deploy_render.bat
```

#### On Linux/Mac:
```bash
chmod +x deploy_render.sh
./deploy_render.sh
```

### Option 2: Manual Deployment

```bash
# Deploy using render.yaml configuration
render up

# Follow the prompts to select/create service
```

## Configuration

The `render.yaml` file contains all deployment configuration:

```yaml
services:
  - type: web
    name: cricket-scraper-api
    env: python
    region: oregon  # Change to your preferred region
    plan: starter   # Change to your preferred plan
    branch: main    # Your deployment branch
```

### Environment Variables

The following environment variables are pre-configured in `render.yaml`:

- `PYTHON_VERSION`: 3.11.0
- `HOST`: 0.0.0.0
- `PORT`: 10000 (Render default)
- `WORKERS`: 4
- `APP_NAME`: Cricket Odds API
- `VERSION`: 1.0.0
- `BASE_URL`: https://api.radheexch.xyz
- `SCRAPE_INTERVAL`: 5 (seconds)
- `LOG_LEVEL`: INFO

### Setting ALLOWED_DOMAINS

After deployment, you **must** set the `ALLOWED_DOMAINS` environment variable in the Render Dashboard:

1. Go to your service in the Render Dashboard
2. Navigate to **Environment** tab
3. Add a new environment variable:
   - Key: `ALLOWED_DOMAINS`
   - Value: `https://your-domain.com,https://another-domain.com`
4. Save and redeploy

Or using CLI:
```bash
render env set ALLOWED_DOMAINS="https://your-domain.com,https://another-domain.com"
```

## Persistent Storage

The configuration includes a persistent disk for storing JSON data files:

```yaml
disk:
  name: cricket-data
  mountPath: /opt/render/project/src/app/data
  sizeGB: 1
```

This ensures your `all_matches.json` and `live_matches.json` files persist across deployments.

## Monitoring

### View Logs
```bash
# Stream logs in real-time
render logs -f

# View last 100 log lines
render logs --tail 100
```

### Check Service Status
```bash
render services list
```

### Open Service in Browser
```bash
render open
```

## Updating Your Application

### Deploy Updates
```bash
# Make your code changes
git add .
git commit -m "Update description"
git push origin main

# Trigger manual deployment
render deploy
```

Render will automatically deploy when you push to your configured branch (default: main).

## Troubleshooting

### Deployment Fails

1. **Check logs**:
   ```bash
   render logs --tail 200
   ```

2. **Validate render.yaml**:
   ```bash
   render validate
   ```

3. **Check build output** in the Render Dashboard

### Service Won't Start

1. Verify all environment variables are set correctly
2. Check that `requirements.txt` includes all dependencies
3. Ensure the start command is correct
4. Review application logs for errors

### Data Not Persisting

1. Verify disk is mounted correctly in `render.yaml`
2. Check that your application writes to the correct path: `/opt/render/project/src/app/data`
3. Ensure disk size is sufficient

## CLI Commands Reference

```bash
# Authentication
render login
render logout

# Deployment
render up                    # Deploy service from render.yaml
render deploy                # Trigger manual deployment
render validate              # Validate render.yaml

# Service Management
render services list         # List all services
render services show <name>  # Show service details
render open                  # Open service in browser

# Logs
render logs -f              # Follow logs
render logs --tail 100      # Last 100 lines

# Environment Variables
render env list             # List environment variables
render env set KEY=value    # Set environment variable
render env unset KEY        # Remove environment variable

# Shell Access
render shell                # Open shell in service
```

## Pricing

- **Starter Plan**: Free tier available with limitations
- **Professional Plans**: Starting at $7/month
- Visit [Render Pricing](https://render.com/pricing) for details

## Support

- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Support Portal](https://render.com/support)

## Additional Resources

- [Render CLI Documentation](https://render.com/docs/cli)
- [Render Blueprint Specification](https://render.com/docs/blueprint-spec)
- [Python Deployment Guide](https://render.com/docs/deploy-fastapi)
