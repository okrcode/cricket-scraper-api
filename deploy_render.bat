@echo off
REM =====================================================
REM Render Deployment Script for Windows
REM =====================================================
REM This script deploys the Cricket Scraper API to Render
REM using the Render CLI.
REM =====================================================

echo ====================================================
echo  Render Deployment Script for Cricket Scraper API
echo ====================================================
echo.

REM Check if Render CLI is installed
where render >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Render CLI not found!
    echo.
    echo Please install the Render CLI first:
    echo   npm install -g @render-cloud/cli
    echo.
    echo Or download from: https://render.com/docs/cli
    echo.
    pause
    exit /b 1
)

echo Step 1: Checking Render CLI installation...
render --version
if %errorlevel% neq 0 (
    echo ERROR: Render CLI check failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Authenticating with Render...
echo Please make sure you are logged in to Render.
echo If not, run: render login
echo.
pause

echo Step 3: Validating render.yaml configuration...
if not exist render.yaml (
    echo ERROR: render.yaml not found!
    echo Please make sure render.yaml exists in the project root.
    pause
    exit /b 1
)
echo Configuration file found: render.yaml
echo.

echo Step 4: Deploying to Render...
echo This will create/update your service based on render.yaml
echo.
render up
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Deployment failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo  Deployment completed successfully!
echo ====================================================
echo.
echo Next steps:
echo 1. Check your Render dashboard for deployment status
echo 2. Set the ALLOWED_DOMAINS environment variable in Render dashboard
echo 3. Monitor logs: render logs -f
echo.
pause
