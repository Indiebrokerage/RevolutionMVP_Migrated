#!/bin/bash
# Unified deployment script for Railway
# This script builds the React frontend and serves it through Django

echo "🚀 Starting Unified Deployment (React + Django)..."

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Trying to install Node.js..."
    # Try to install Node.js if not available
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y nodejs npm
    elif command -v yum &> /dev/null; then
        yum install -y nodejs npm
    else
        echo "❌ Cannot install Node.js. Skipping React build."
        SKIP_REACT=true
    fi
fi

# Step 1: Build React Frontend (if npm is available)
if [ "$SKIP_REACT" != "true" ] && command -v npm &> /dev/null; then
    echo "📦 Building React Frontend..."
    cd frontend/
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
        echo '<html><head><title>RevolutionMVP</title></head><body><h1>React build in progress...</h1></body></html>' > backend/core/templates/index.html
    fi
    
    # Step 3: Copy React assets to Django static directory
    echo "📁 Copying React assets to Django static..."
    mkdir -p backend/staticfiles
    if [ -d "frontend/dist/assets" ]; then
        cp -r frontend/dist/assets/* backend/staticfiles/
        echo "✅ React assets copied to Django static files"
    else
        echo "⚠️ No React assets directory found"
    fi
else
    echo "⚠️ Skipping React build - npm not available"
    # Create fallback template
    mkdir -p backend/core/templates
    echo '<html><head><title>RevolutionMVP</title></head><body><h1>Django Backend Running</h1><p>React frontend will be available soon.</p><p><a href="/api/">API</a> | <a href="/admin/">Admin</a></p></body></html>' > backend/core/templates/index.html
fi

# Step 4: Install Python dependencies from root
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 5: Collect static files (includes React build)
echo "📁 Collecting static files..."
cd backend/
python3 manage.py collectstatic --noinput || python manage.py collectstatic --noinput
echo "✅ Static files collected"

# Step 6: Run database migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate --noinput || python manage.py migrate --noinput
echo "✅ Database migrations completed"

# Step 7: Start Django server
echo "🌟 Starting Django server (serving React frontend + API)..."
exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

