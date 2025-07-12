from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render
import os

def react_frontend_view(request):
    """Serve React frontend or fallback message"""
    try:
        # Try to serve the React index.html
        return render(request, 'index.html')
    except:
        # Fallback if React build is not available
        return HttpResponse("""
        <html>
        <head><title>RevolutionMVP</title></head>
        <body>
            <h1>RevolutionMVP Application</h1>
            <p>The application is running, but the React frontend is not yet available.</p>
            <p>API endpoints are available at <a href="/api/">/api/</a></p>
            <p>Admin interface is available at <a href="/admin/">/admin/</a></p>
        </body>
        </html>
        """)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),  # All API routes under /api/
    # Serve React frontend for all other routes
    re_path(r'^.*$', react_frontend_view, name='react_frontend'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


