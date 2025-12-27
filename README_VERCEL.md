# Vercel Deployment Guide for Brownie Shop

This guide explains how to deploy the Brownie Shop application to Vercel.

## Files Created for Vercel

### 1. `app.py`
- Main FastAPI application entry point for Vercel
- Contains all the API routes and functionality
- Uses relative paths for static files

### 2. `vercel.json`
- Vercel configuration file
- Defines build settings and routing
- Sets up environment variable references

### 3. `runtime.txt`
- Specifies Python version (3.11)

### 4. `.vercelignore`
- Files and folders to ignore during deployment

## Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables
In your Vercel dashboard or via CLI, set these environment variables:

```bash
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY  
vercel env add SUPABASE_SERVICE_KEY
vercel env add SECRET_KEY
vercel env add ADMIN_EMAIL
vercel env add ADMIN_PASSWORD
```

Use the values from your `.env` file:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `SUPABASE_SERVICE_KEY`: Your Supabase service key
- `SECRET_KEY`: JWT secret key
- `ADMIN_EMAIL`: admin@brownieshop.com
- `ADMIN_PASSWORD`: admin123

### 4. Deploy
```bash
vercel --prod
```

## Important Notes

### Database Setup
1. Make sure your Supabase database is set up with the tables from `database_setup.sql`
2. The application will connect to your Supabase instance automatically

### File Uploads
- Image uploads will work but files are stored temporarily on Vercel
- For production, consider using Supabase Storage or another cloud storage service
- Current implementation stores files in `/tmp` which is cleared between deployments

### Static Files
- Frontend files are served from the `frontend/` directory
- CSS, JS, and HTML files are included in the deployment

### Environment Variables
- Never commit your `.env` file to version control
- Set all environment variables in Vercel dashboard
- Use strong, unique values for production

## Production Considerations

### 1. Image Storage
For production, replace local file storage with cloud storage:
```python
# Consider using Supabase Storage
from supabase import create_client
storage = supabase.storage.from_('product-images')
```

### 2. Security
- Use strong, unique SECRET_KEY
- Change default admin credentials
- Enable HTTPS (Vercel provides this automatically)

### 3. Database
- Your Supabase database is already production-ready
- Consider setting up database backups
- Monitor database usage and performance

## Troubleshooting

### Common Issues

1. **Environment Variables Not Found**
   - Check Vercel dashboard environment variables
   - Ensure all required variables are set

2. **Database Connection Issues**
   - Verify Supabase URL and keys
   - Check Supabase project status

3. **Static Files Not Loading**
   - Ensure `frontend/` directory is included in deployment
   - Check `vercel.json` routing configuration

4. **Image Upload Issues**
   - Temporary storage limitations on Vercel
   - Consider implementing cloud storage

## Local Testing

To test the Vercel-ready version locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The application will be available at `http://localhost:8000`

## Deployment URL

After successful deployment, Vercel will provide you with:
- Production URL: `https://your-app-name.vercel.app`
- Preview URLs for each deployment

Your brownie shop will be live and accessible worldwide!