#!/bin/bash
# Backend deployment script for Railway
# This script deploys the Django backend application

echo "🚀 Deploying Django Backend..."

# Navigate to backend directory
cd backend/

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django application with Gunicorn
echo "🌟 Starting Django application..."
exec gunicorn RevolutionMVP_Django.wsgi --log-file - --bind 0.0.0.0:$PORT

