# RevolutionMVP - Migrated to Django/React

This repository contains the migrated RevolutionMVP application, converted from Laravel/PHP to a modern Django/React stack.

## Repository Structure

```
RevolutionMVP_Migrated/
├── backend/          # Django REST API backend
│   ├── core/         # Django app with models, views, URLs
│   ├── RevolutionMVP_Django/  # Django project settings
│   ├── requirements.txt       # Python dependencies
│   ├── railway.json          # Railway deployment config
│   └── Procfile              # Process file for deployment
├── frontend/         # React frontend application
│   ├── src/          # React source code
│   ├── public/       # Static assets
│   ├── package.json  # Node.js dependencies
│   ├── railway.json  # Railway deployment config
│   └── Procfile      # Process file for deployment
└── railway.json      # Root Railway configuration
```

## Technology Stack

### Backend (Django)
- **Framework**: Django 5.2.4
- **Database**: MySQL/PostgreSQL
- **API**: Django REST Framework
- **Authentication**: Django built-in auth system
- **Deployment**: Gunicorn WSGI server

### Frontend (React)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Routing**: React Router
- **State Management**: React Hooks

## Railway Deployment Instructions

This is a **monorepo** containing both backend and frontend applications. You need to deploy them as **separate services** on Railway.

### Step 1: Create Backend Service
1. Go to your Railway project dashboard
2. Click "New Service" → "GitHub Repo"
3. Select this repository (`RevolutionMVP_Migrated`)
4. **Important**: Set the **Root Directory** to `backend/`
5. Railway will automatically detect the Django application and use the `railway.json` configuration

### Step 2: Create Frontend Service
1. In the same Railway project, click "New Service" → "GitHub Repo"
2. Select this repository (`RevolutionMVP_Migrated`) again
3. **Important**: Set the **Root Directory** to `frontend/`
4. Railway will automatically detect the React application and use the `railway.json` configuration

### Step 3: Configure Environment Variables

#### Backend Environment Variables
Set these in your Django backend service:
- `DATABASE_URL`: Your database connection string
- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Your Railway domain

#### Frontend Environment Variables
Set these in your React frontend service:
- `VITE_API_URL`: URL of your deployed Django backend service

### Step 4: Database Setup
1. Add a database service to your Railway project (PostgreSQL recommended)
2. The `DATABASE_URL` will be automatically provided to your backend service
3. Run migrations: `python manage.py migrate`

## Local Development

### Backend Setup
```bash
cd backend/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend/
npm install
npm run dev
```

## Features

- **Property Management**: Create, read, update, delete property listings
- **User Authentication**: Secure user registration and login
- **Responsive Design**: Mobile-first, responsive UI
- **Modern Architecture**: Clean separation of concerns
- **API-First**: RESTful API design
- **Production Ready**: Configured for cloud deployment

## Migration Notes

This application was successfully migrated from:
- **Laravel 5.x/PHP** → **Django 5.2.4/Python 3.11**
- **Blade Templates** → **React 18 with Tailwind CSS**
- **MySQL** → **PostgreSQL/MySQL (compatible with both)**

All original functionality has been preserved and enhanced with modern development practices.

