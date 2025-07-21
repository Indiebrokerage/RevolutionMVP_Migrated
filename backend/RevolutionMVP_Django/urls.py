from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.urls import api_urlpatterns
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes
    path("api/", include(api_urlpatterns)),
    # React frontend for all other routes
    re_path(r'^.*$', views.react_frontend, name='react_frontend'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


