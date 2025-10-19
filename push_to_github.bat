@echo off
REM =====================================================
REM Push Cricket Scraper to GitHub
REM =====================================================

echo ====================================================
echo  Push Cricket Scraper API to GitHub
echo ====================================================
echo.

REM Set Git path
set PATH=C:\Program Files\Git\cmd;%PATH%

REM Navigate to project directory
cd /d "%~dp0"

echo Please enter your GitHub repository URL
echo Example: https://github.com/username/cricket-scraper-api.git
echo.
set /p REPO_URL="GitHub Repository URL: "

if "%REPO_URL%"=="" (
    echo.
    echo ERROR: No repository URL provided!
    pause
    exit /b 1
)

echo.
echo ====================================================
echo  Configuring Git remote...
echo ====================================================

REM Remove existing remote if exists
git remote remove origin 2>nul

REM Add new remote
git remote add origin %REPO_URL%

if %errorlevel% neq 0 (
    echo ERROR: Failed to add remote repository!
    pause
    exit /b 1
)

echo ✓ Remote repository configured
echo.

echo ====================================================
echo  Pushing to GitHub...
echo ====================================================
echo.
echo You may be prompted for GitHub credentials:
echo - Username: Your GitHub username
echo - Password: Use a Personal Access Token (not password)
echo   Create token at: https://github.com/settings/tokens
echo.

git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ====================================================
    echo  Push Failed!
    echo ====================================================
    echo.
    echo Common issues:
    echo 1. Incorrect repository URL
    echo 2. Authentication failed - use Personal Access Token
    echo 3. Repository already has content
    echo.
    echo To create a Personal Access Token:
    echo 1. Go to https://github.com/settings/tokens
    echo 2. Click "Generate new token" (classic)
    echo 3. Select "repo" scope
    echo 4. Copy the token and use it as your password
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo  ✓ Successfully pushed to GitHub!
echo ====================================================
echo.
echo Next steps:
echo 1. Go to https://dashboard.render.com
echo 2. Click "New +" → "Blueprint"
echo 3. Connect your GitHub account
echo 4. Select your repository
echo 5. Click "Apply"
echo.
echo Your app will be deployed automatically!
echo See RENDER_DEPLOY_STEPS.md for detailed instructions.
echo.
pause
