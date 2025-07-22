from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.admin import admin_site  # Import custom admin site

urlpatterns = [
    path("admin/", admin_site.urls),  # Use custom SaaS admin site
    # Include core app URLs (which includes API routes)
    path("", include('core.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


