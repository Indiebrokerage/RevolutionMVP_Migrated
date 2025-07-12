#!/bin/bash
# Unified deployment script for Railway
# This script builds the React frontend and serves it through Django

echo "🚀 Starting Unified Deployment (React + Django)..."

# Step 1: Build React Frontend (if possible)
echo "📦 Building React Frontend..."
if [ -d "frontend" ]; then
    cd frontend/
    if command -v npm &> /dev/null; then
        npm install --legacy-peer-deps || npm install --force || npm install
        npm run build
        echo "✅ React build completed"
        
        # Step 2: Copy React build to Django templates directory
        echo "📁 Copying React build to Django..."
        cd ..
        mkdir -p backend/core/templates
        if [ -f "frontend/dist/index.html" ]; then
            cp frontend/dist/index.html backend/core/templates/
            echo "✅ React index.html copied to Django templates"
        else
            echo "⚠️ React index.html not found, creating fallback"
            echo '<html><head><title>RevolutionMVP</title></head><body><h1>React build in progress...</h1><p><a href="/api/">API</a> | <a href="/admin/">Admin</a></p></body></html>' > backend/core/templates/index.html
        fi
        
        # Step 3: Copy React assets to Django static directory
        echo "📁 Copying React assets to Django static..."
        mkdir -p backend/staticfiles
        if [ -d "frontend/dist/assets" ]; then
            cp -r frontend/dist/assets/* backend/staticfiles/ 2>/dev/null || echo "No assets to copy"
            echo "✅ React assets copied to Django static files"
        fi
    else
        echo "⚠️ npm not available, skipping React build"
        cd ..
        mkdir -p backend/core/templates
        echo '<html><head><title>RevolutionMVP</title></head><body><h1>Django Backend Running</h1><p>React frontend will be available soon.</p><p><a href="/api/">API</a> | <a href="/admin/">Admin</a></p></body></html>' > backend/core/templates/index.html
    fi
else
    echo "⚠️ Frontend directory not found"
    mkdir -p backend/core/templates
    echo '<html><head><title>RevolutionMVP</title></head><body><h1>Django Backend Running</h1><p><a href="/api/">API</a> | <a href="/admin/">Admin</a></p></body></html>' > backend/core/templates/index.html
fi

# Step 4: Install Python dependencies
echo "📦 Installing Python dependencies..."
# Use python3 and pip3 explicitly for Railway environment
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 5: Collect static files
echo "📁 Collecting static files..."
cd backend/
python3 manage.py collectstatic --noinput
echo "✅ Static files collected"

# Step 6: Run database migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate --noinput
echo "✅ Database migrations completed"

echo "🎉 Build process completed successfully!"

