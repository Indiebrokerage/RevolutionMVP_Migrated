#!/bin/bash
# Frontend deployment script for Railway
# This script deploys the React frontend application

echo "🚀 Deploying React Frontend..."

# Navigate to frontend directory
cd frontend/

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build the React application
echo "🏗️ Building React application..."
npm run build

# Start the application in preview mode
echo "🌟 Starting React application..."
exec npm run preview -- --host 0.0.0.0 --port $PORT

