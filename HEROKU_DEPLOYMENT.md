# Inner Veda Tea Store - Heroku Deployment Guide

## 🍃 Backend Deployment to Heroku

This guide will help you deploy the Inner Veda Tea Store FastAPI backend to Heroku.

### Prerequisites

1. **Heroku CLI** installed on your system
2. **Git** repository initialized
3. **Heroku account** created

### Required Files (✅ Created)

- `Procfile` - Tells Heroku how to start your FastAPI app
- `requirements.txt` - Python dependencies (updated with gunicorn)
- `runtime.txt` - Specifies Python 3.11.5 version
- `deploy-heroku.sh` - Automated deployment script

### Deployment Steps

#### Option 1: Automated Deployment (Recommended)

```bash
# Make the script executable (on Unix systems)
chmod +x deploy-heroku.sh

# Run the deployment script
./deploy-heroku.sh
```

#### Option 2: Manual Deployment

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create innerveda-tea-api
   ```

3. **Set Python Buildpack**
   ```bash
   heroku buildpacks:clear -a innerveda-tea-api
   heroku buildpacks:add heroku/python -a innerveda-tea-api
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set ENVIRONMENT=production -a innerveda-tea-api
   heroku config:set MONGODB_URL="mongodb+srv://teawebsite:teawebsite123@teawebsite.ezdqheb.mongodb.net/?retryWrites=true&w=majority&appName=teawebsite" -a innerveda-tea-api
   heroku config:set DATABASE_NAME="teawebsite" -a innerveda-tea-api
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy Inner Veda Tea Store API to Heroku"
   git push heroku main
   ```

6. **Scale Web Dyno**
   ```bash
   heroku ps:scale web=1 -a innerveda-tea-api
   ```

### Procfile Configuration

The `Procfile` is configured for your FastAPI app structure:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Alternative Procfile options:**

For better production performance with multiple workers:
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT
```

### Environment Variables

The following environment variables are configured:

- `ENVIRONMENT=production` - Sets production mode
- `MONGODB_URL` - MongoDB Atlas connection string
- `DATABASE_NAME=teawebsite` - Database name

### CORS Configuration

The main.py file has been updated with production-ready CORS settings:

- ✅ `https://innerveda.netlify.app` (Frontend)
- ✅ `https://innerveda.in` (Custom domain)
- ✅ `https://www.innerveda.in` (WWW variant)
- ✅ `http://localhost:3000` (Local development)

### Health Check Endpoints

- **Root**: `https://innerveda-tea-api.herokuapp.com/`
- **Health**: `https://innerveda-tea-api.herokuapp.com/health`
- **API Docs**: `https://innerveda-tea-api.herokuapp.com/docs`

### Monitoring & Debugging

```bash
# View logs
heroku logs --tail -a innerveda-tea-api

# Check dyno status
heroku ps -a innerveda-tea-api

# Restart app
heroku restart -a innerveda-tea-api
```

### Troubleshooting

1. **Build Fails**: Check `requirements.txt` for correct dependencies
2. **App Crashes**: Check logs with `heroku logs --tail`
3. **Port Issues**: Ensure Procfile uses `$PORT` variable
4. **CORS Issues**: Verify allowed origins in main.py

### Production Checklist

- [x] Procfile created with correct uvicorn command
- [x] requirements.txt includes all dependencies + gunicorn
- [x] runtime.txt specifies Python 3.11.5
- [x] CORS configured for production domains
- [x] Health check endpoints added
- [x] MongoDB Atlas connection configured
- [x] Environment variables set

### Next Steps

After successful deployment:

1. Update frontend `lib/api.ts` to use production API URL
2. Test all API endpoints
3. Configure custom domain (optional)
4. Set up monitoring and alerts

### Support

- **API URL**: `https://innerveda-tea-api.herokuapp.com`
- **Admin**: hkchakravarty@gmail.com
- **Support**: innervedacare@gmail.com
