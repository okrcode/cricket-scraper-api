#!/usr/bin/env bash
# =====================================================
# Render Deployment Script for Unix/Linux/Mac
# =====================================================
# This script deploys the Cricket Scraper API to Render
# using the Render CLI.
# =====================================================

set -e  # Exit on error

echo "===================================================="
echo " Render Deployment Script for Cricket Scraper API"
echo "===================================================="
echo ""

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ ERROR: Render CLI not found!"
    echo ""
    echo "Please install the Render CLI first:"
    echo "  npm install -g @render-cloud/cli"
    echo ""
    echo "Or download from: https://render.com/docs/cli"
    echo ""
    exit 1
fi

echo "✅ Step 1: Checking Render CLI installation..."
render --version
echo ""

echo "🔐 Step 2: Authenticating with Render..."
echo "Please make sure you are logged in to Render."
echo "If not, run: render login"
echo ""
read -p "Press Enter to continue..."

echo "📋 Step 3: Validating render.yaml configuration..."
if [ ! -f render.yaml ]; then
    echo "❌ ERROR: render.yaml not found!"
    echo "Please make sure render.yaml exists in the project root."
    exit 1
fi
echo "✅ Configuration file found: render.yaml"
echo ""

echo "🚀 Step 4: Deploying to Render..."
echo "This will create/update your service based on render.yaml"
echo ""
render up

echo ""
echo "===================================================="
echo " ✅ Deployment completed successfully!"
echo "===================================================="
echo ""
echo "Next steps:"
echo "1. Check your Render dashboard for deployment status"
echo "2. Set the ALLOWED_DOMAINS environment variable in Render dashboard"
echo "3. Monitor logs: render logs -f"
echo ""
