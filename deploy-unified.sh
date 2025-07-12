#!/bin/bash
# Unified deployment script for Railway
# This script builds the React frontend and serves it through Django

set -e  # Exit on any error

echo "🚀 Starting Unified Deployment (React + Django)..."

# Check if we're in the right directory
if [ ! -f "deploy-unified.sh" ]; then
    echo "Error: Not in the correct directory"
    exit 1
fi

# Step 1: Build React Frontend (if not already built)
if [ ! -d "frontend/dist" ]; then
    echo "📦 Building React Frontend..."
    cd frontend/
    npm install --legacy-peer-deps
    npm run build
    cd ..
    echo "✅ React build completed"
else
    echo "✅ React build already exists"
fi

# Step 2: Move to backend and install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend/

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip not found. Trying pip3..."
    if ! command -v pip3 &> /dev/null; then
        echo "Error: Neither pip nor pip3 found"
        exit 1
    else
        pip3 install -r requirements.txt
    fi
else
    pip install -r requirements.txt
fi
echo "✅ Python dependencies installed"

# Step 3: Collect static files (includes React build)
echo "📁 Collecting static files..."
if command -v python &> /dev/null; then
    python manage.py collectstatic --noinput
elif command -v python3 &> /dev/null; then
    python3 manage.py collectstatic --noinput
else
    echo "Error: Python not found"
    exit 1
fi
echo "✅ Static files collected"

# Step 4: Run database migrations
echo "🗄️ Running database migrations..."
if command -v python &> /dev/null; then
    python manage.py migrate --noinput
elif command -v python3 &> /dev/null; then
    python3 manage.py migrate --noinput
else
    echo "Error: Python not found"
    exit 1
fi
echo "✅ Database migrations completed"

# Step 5: Start Django server
echo "🌟 Starting Django server (serving React frontend + API)..."
if command -v gunicorn &> /dev/null; then
    exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT
else
    echo "Error: gunicorn not found. Trying to install..."
    if command -v pip &> /dev/null; then
        pip install gunicorn
    elif command -v pip3 &> /dev/null; then
        pip3 install gunicorn
    else
        echo "Error: Cannot install gunicorn"
        exit 1
    fi
    exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT
fi

