# Revolution Realty - URL Configuration
# Comprehensive API routing for frontend integration

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'leads', views.LeadViewSet)
router.register(r'lead-sources', views.LeadSourceViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'task-boards', views.TaskBoardViewSet)
router.register(r'task-lists', views.TaskListViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'property-images', views.PropertyImageViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'site-settings', views.SiteSettingsViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # Frontend Routes (React)
    path('', views.home_view, name='home'),
    
    # API Routes
    path('api/', views.api_welcome, name='api_welcome'),
    path('api/', include(router.urls)),
    
    # Dashboard & Analytics
    path('api/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/lead-sources/', views.lead_source_performance, name='lead_source_performance'),
    path('api/dashboard/monthly/', views.monthly_performance, name='monthly_performance'),
    
    # Public API Endpoints
    path('api/public/capture-lead/', views.capture_lead, name='capture_lead'),
    path('api/public/property-search/', views.property_search, name='property_search'),
]

