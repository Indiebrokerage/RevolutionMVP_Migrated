#!/bin/bash
# Unified deployment script for Railway
# This script builds the React frontend and serves it through Django

echo "🚀 Starting Unified Deployment (React + Django)..."

# Step 1: Build React Frontend
echo "📦 Building React Frontend..."
cd frontend/
npm install --legacy-peer-deps
npm run build
echo "✅ React build completed"

# Step 2: Move to backend and install Python dependencies
echo "📦 Installing Python dependencies..."
cd ../backend/
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 3: Collect static files (includes React build)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput
echo "✅ Static files collected"

# Step 4: Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput
echo "✅ Database migrations completed"

# Step 5: Start Django server
echo "🌟 Starting Django server (serving React frontend + API)..."
exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

