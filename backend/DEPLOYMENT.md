# Deployment Guide - Railway

## Prerequisites
- Railway account (https://railway.app)
- Git repository with the Django project
- Railway CLI (optional)

## Step 1: Prepare the Project

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Ensure all dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations locally to verify:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for testing):**
   ```bash
   python manage.py create_superuser
   ```

## Step 2: Push to Git

1. **Initialize git if not already done:**
   ```bash
   git init
   git add .
   git commit -m "Ready for Railway deployment"
   ```

2. **Push to GitHub/GitLab/Bitbucket:**
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

## Step 3: Deploy to Railway

### Option A: Via Railway Web Interface

1. Go to [Railway](https://railway.app) and log in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the Python project
5. Click "Deploy"

### Option B: Via Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Initialize:**
   ```bash
   railway init
   ```

4. **Add PostgreSQL database:**
   ```bash
   railway add postgresql
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

## Step 4: Configure Environment Variables

In Railway dashboard, go to your project → Settings → Variables and add:

```
DEBUG=False
SECRET_KEY=<generate a strong secret key>
DB_ENGINE=postgresql
DB_NAME=${{RAILWAY_POSTGRES_DB_NAME}}
DB_USER=${{RAILWAY_POSTGRES_USER}}
DB_PASSWORD=${{RAILWAY_POSTGRES_PASSWORD}}
DB_HOST=${{RAILWAY_POSTGRES_HOST}}
DB_PORT=${{RAILWAY_POSTGRES_PORT}}
DB_CONN_MAX_AGE=60
CORS_ALLOWED_ORIGINS=<your-frontend-domain>
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
JWT_ACCESS_TOKEN_HOURS=2
JWT_REFRESH_TOKEN_DAYS=7
ALLOWED_HOSTS=<your-railway-domain>.railway.app
```

**Note:** Railway automatically provides PostgreSQL connection details as environment variables (RAILWAY_POSTGRES_*).

## Step 5: Run Migrations on Railway

After deployment, you need to run migrations:

1. Go to Railway dashboard → your project
2. Click on the "Console" tab for your web service
3. Run:
   ```bash
   python manage.py migrate
   ```

## Step 6: Create Superuser

In the Railway console:

```bash
python manage.py create_superuser
```

Follow the prompts to create your admin account.

## Step 7: Verify Deployment

1. Get your Railway URL from the dashboard
2. Visit `https://<your-app>.railway.app/api/health/`
3. You should see: `{"status": "healthy"}`

## Step 8: Update Frontend Configuration

Update the API URL in your frontend (`Js/api-client.js`):

```javascript
const API_BASE_URL = 'https://<your-app>.railway.app/api';
```

## Troubleshooting

### Build Failures
- Check the build logs in Railway dashboard
- Ensure `requirements.txt` is in the Django directory
- Verify Python version compatibility

### Database Connection Issues
- Verify all database environment variables are set
- Check that PostgreSQL addon is running
- Ensure DB_ENGINE is set to `postgresql`

### CORS Errors
- Add your frontend domain to `CORS_ALLOWED_ORIGINS`
- For local development, you can temporarily set `CORS_ALLOW_ALL_ORIGINS=True`

### Static Files
- Static files are served via Whitenoise
- If needed, run `python manage.py collectstatic` in Railway console

## Monitoring

- Check logs in Railway dashboard
- Monitor PostgreSQL usage in the database tab
- Set up alerts for errors and performance issues

## Security Notes

- Never commit `.env` file
- Use strong `SECRET_KEY` (generate with: `python manage.py generatesecretkey`)
- Keep `DEBUG=False` in production
- Use HTTPS (Railway provides this automatically)
- Regularly update dependencies
