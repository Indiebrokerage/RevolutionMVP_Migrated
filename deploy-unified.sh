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

# Step 2: Copy React build to Django templates directory
echo "📁 Copying React build to Django..."
cd ..
mkdir -p backend/core/templates
cp frontend/dist/index.html backend/core/templates/
echo "✅ React index.html copied to Django templates"

# Step 3: Copy React assets to Django static directory
echo "📁 Copying React assets to Django static..."
mkdir -p backend/staticfiles
if [ -d "frontend/dist/assets" ]; then
    cp -r frontend/dist/assets/* backend/staticfiles/
    echo "✅ React assets copied to Django static files"
else
    echo "⚠️ No React assets directory found"
fi

# Step 4: Install Python dependencies from root
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 5: Collect static files (includes React build)
echo "📁 Collecting static files..."
cd backend/
python3 manage.py collectstatic --noinput
echo "✅ Static files collected"

# Step 6: Run database migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate --noinput
echo "✅ Database migrations completed"

# Step 7: Start Django server
echo "🌟 Starting Django server (serving React frontend + API)..."
exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

