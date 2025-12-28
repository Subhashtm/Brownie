# Deployment Guide

## Fixed Issues

### 1. Import Error Fix
- Made all dependencies optional with graceful fallbacks
- Added proper error handling for missing packages
- App will now start even if some dependencies are missing

### 2. Supabase Connection
- Added connection error handling
- App will run in limited mode if database is unavailable
- Added health check endpoint to verify connection status

### 3. Image Processing
- Made PIL (Pillow) optional for image optimization
- App will skip image optimization if PIL is not available
- Added fallback for older Pillow versions

## Health Check Endpoint

Visit `/health` to check the app status:
```json
{
  "status": "healthy",
  "supabase_connected": true,
  "dependencies": {
    "supabase": true,
    "jwt": true,
    "bcrypt": true,
    "pil": true
  },
  "environment_vars": {
    "SUPABASE_URL": true,
    "SUPABASE_KEY": true,
    "SECRET_KEY": true,
    "ADMIN_EMAIL": true
  }
}
```

## Troubleshooting Steps

### 1. Check Environment Variables
Make sure all required environment variables are set in your deployment platform:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SECRET_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

### 2. Database Setup
Run the SQL commands in `database_setup.sql` in your Supabase SQL editor to create the required tables.

### 3. Test Endpoints
- `/health` - Check app health and dependencies
- `/api/test` - Test basic API functionality
- `/` - Load the frontend

### 4. Common Issues

#### "Error importing app.py"
- Check that all dependencies in `requirements.txt` are available
- Verify environment variables are set
- Check the health endpoint for specific issues

#### "Database not available"
- Verify Supabase URL and key are correct
- Check that database tables exist
- Run the database setup SQL

#### "JWT not available" or "Password hashing not available"
- Check that all packages in requirements.txt are installed
- Verify the deployment platform supports all dependencies

## Files Overview

- `app.py` - Main application with error handling
- `minimal_app.py` - Minimal version for testing
- `test_app.py` - Simple test app
- `debug_startup.py` - Diagnostic script
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration

## Deployment Platforms

### Vercel
1. Connect your GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy using the existing `vercel.json` configuration

### Other Platforms
The app should work on any platform that supports Python and FastAPI:
- Railway
- Render
- Heroku
- DigitalOcean App Platform

## Email Configuration (Optional)

For payment receipt notifications, add these environment variables:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

If email is not configured, the app will still work but won't send notifications.