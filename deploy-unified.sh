#!/bin/bash
# Unified deployment script for Railway
# This script builds the React frontend and serves it through Django

echo "🚀 Starting Unified Deployment (React + Django)..."

# Step 1: Build React Frontend
echo "📦 Building React Frontend..."
cd frontend/
npm install --legacy-peer-deps
npm run build
cd ..
echo "✅ React build completed"

# Step 2: Install Python dependencies from root
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 3: Collect static files (includes React build)
echo "📁 Collecting static files..."
cd backend/
python3 manage.py collectstatic --noinput
echo "✅ Static files collected"

# Step 4: Run database migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate --noinput
echo "✅ Database migrations completed"

# Step 5: Start Django server
echo "🌟 Starting Django server (serving React frontend + API)..."
exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

