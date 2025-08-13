#!/bin/bash

# Inner Veda Tea Store - Heroku Deployment Script
# This script automates the deployment of the FastAPI backend to Heroku

APP_NAME="teawebsite"
HEROKU_REMOTE="heroku"

echo "🍃 Starting Inner Veda Tea Store Backend Deployment to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first."
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "🔐 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Create Heroku app if it doesn't exist
echo "🏗️ Creating/checking Heroku app: $APP_NAME"
heroku apps:info $APP_NAME 2>/dev/null || heroku create $APP_NAME

# Set Python buildpack
echo "🐍 Setting Python buildpack..."
heroku buildpacks:clear -a $APP_NAME
heroku buildpacks:add heroku/python -a $APP_NAME

# Set environment variables for production
echo "🔧 Setting environment variables..."
heroku config:set ENVIRONMENT=production -a $APP_NAME
heroku config:set MONGODB_URL="mongodb+srv://teawebsite:teawebsite123@teawebsite.ezdqheb.mongodb.net/?retryWrites=true&w=majority&appName=teawebsite" -a $APP_NAME
heroku config:set DATABASE_NAME="teawebsite" -a $APP_NAME

# Optional: Set additional environment variables
# heroku config:set OPENAI_API_KEY="your-openai-key" -a $APP_NAME
# heroku config:set REDIS_URL="your-redis-url" -a $APP_NAME

# Add Heroku remote if it doesn't exist
if ! git remote get-url $HEROKU_REMOTE &> /dev/null; then
    echo "📡 Adding Heroku remote..."
    heroku git:remote -a $APP_NAME -r $HEROKU_REMOTE
fi

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy Inner Veda Tea Store API to Heroku" || echo "No changes to commit"
git push $HEROKU_REMOTE main

# Scale web dyno
echo "⚡ Scaling web dyno..."
heroku ps:scale web=1 -a $APP_NAME

# Show app info
echo "📊 App information:"
heroku apps:info $APP_NAME

# Show logs
echo "📝 Recent logs:"
heroku logs --tail -a $APP_NAME --num 50

echo "✅ Deployment complete!"
echo "🌐 Your API is available at: https://$APP_NAME.herokuapp.com"
echo "🔍 Health check: https://$APP_NAME.herokuapp.com/health"
echo "📚 API docs: https://$APP_NAME.herokuapp.com/docs"
