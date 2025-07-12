# RevolutionMVP - Unified Django/React Deployment

This repository contains the migrated RevolutionMVP application, converted from Laravel/PHP to a modern Django/React stack with **unified deployment** - both frontend and backend served from a single Railway service.

## Repository Structure

```
RevolutionMVP_Migrated/
├── backend/          # Django REST API backend
│   ├── core/         # Django app with models, views, URLs
│   ├── RevolutionMVP_Django/  # Django project settings
│   └── requirements.txt       # Python dependencies
├── frontend/         # React frontend application
│   ├── src/          # React source code
│   ├── public/       # Static assets
│   └── package.json  # Node.js dependencies
├── deploy-unified.sh # Unified deployment script
├── Procfile          # Railway process file
├── railway.json      # Railway configuration
└── README.md         # This file
```

## Technology Stack

### Backend (Django)
- **Framework**: Django 5.2.4
- **Database**: MySQL/PostgreSQL
- **API**: Django REST Framework
- **Authentication**: Django built-in auth system
- **Static Files**: WhiteNoise for serving React build

### Frontend (React)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Routing**: React Router
- **State Management**: React Hooks

## Unified Deployment Architecture

This application uses a **single-service deployment** where:
1. **React frontend** is built into static files
2. **Django backend** serves both the API (under `/api/`) and the React frontend
3. **All routes** not starting with `/api/` or `/admin/` serve the React application
4. **Single Railway service** handles everything

## Railway Deployment Instructions

### Simple One-Click Deployment

1. **Go to Railway** (https://railway.app)
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose this repository**: `RevolutionMVP_Migrated`
5. **Railway will automatically**:
   - Detect the `Procfile` and `railway.json`
   - Run the unified deployment script
   - Build React frontend and Django backend
   - Start the application

### Environment Variables (Optional)

Set these in your Railway project dashboard if needed:
- `SECRET_KEY`: Django secret key (auto-generated if not set)
- `DEBUG`: Set to `False` for production (default)
- `DATABASE_URL`: Automatically provided by Railway database service

### Database Setup

1. **Add a database** to your Railway project (PostgreSQL recommended)
2. **Railway automatically** provides `DATABASE_URL` to your service
3. **Migrations run automatically** during deployment

## Local Development

### Quick Start
```bash
# Backend
cd backend/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (in another terminal)
cd frontend/
npm install
npm run dev
```

### Test Unified Deployment Locally
```bash
# Run the same script Railway uses
./deploy-unified.sh
```

## How It Works

1. **Build Process**: The `deploy-unified.sh` script:
   - Installs Node.js dependencies and builds React
   - Installs Python dependencies
   - Collects static files (includes React build)
   - Runs database migrations
   - Starts Django with Gunicorn

2. **Request Routing**:
   - `/api/*` → Django API endpoints
   - `/admin/*` → Django admin interface
   - `/*` → React frontend (single-page application)

3. **Static Files**: WhiteNoise serves React build files through Django

## Features

- **Single Service**: Simplified deployment and management
- **Cost Effective**: One Railway service instead of two
- **No CORS Issues**: Frontend and backend on same domain
- **Production Ready**: Optimized for cloud deployment
- **Auto-Scaling**: Railway handles scaling automatically

## Migration Notes

Successfully migrated from:
- **Laravel 5.x/PHP** → **Django 5.2.4/Python 3.11**
- **Blade Templates** → **React 18 with Tailwind CSS**
- **Separate Services** → **Unified Single-Service Deployment**

All original functionality preserved with modern development practices and simplified deployment.

