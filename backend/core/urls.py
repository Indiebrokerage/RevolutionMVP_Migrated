# Revolution Realty - URL Configuration
# Comprehensive API routing for frontend integration

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

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
    path('crm/', views.crm_view, name='crm'),
    
    # API Routes
    path('api/', views.api_welcome, name='api_welcome'),
    path('api/', include(router.urls)),
    
    # CRM API Endpoints
    path('api/crm/leads/', api_views.api_leads, name='api_crm_leads'),
    path('api/crm/properties/', api_views.api_properties, name='api_crm_properties'),
    path('api/crm/transactions/', api_views.api_transactions, name='api_crm_transactions'),
    path('api/crm/tasks/', api_views.api_tasks, name='api_crm_tasks'),
    path('api/crm/dashboard/', api_views.api_dashboard_stats, name='api_crm_dashboard'),
    path('api/crm/activities/', api_views.api_activities, name='api_crm_activities'),
    
    # CRUD Operations
    path('api/crm/leads/create/', api_views.api_create_lead, name='api_create_lead'),
    path('api/crm/properties/create/', api_views.api_create_property, name='api_create_property'),
    path('api/crm/tasks/create/', api_views.api_create_task, name='api_create_task'),
    path('api/crm/leads/<int:lead_id>/update/', api_views.api_update_lead, name='api_update_lead'),
    path('api/crm/leads/<int:lead_id>/delete/', api_views.api_delete_lead, name='api_delete_lead'),
    
    # Dashboard & Analytics
    path('api/dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/lead-sources/', views.lead_source_performance, name='lead_source_performance'),
    path('api/dashboard/monthly/', views.monthly_performance, name='monthly_performance'),
    
    # Public API Endpoints
    path('api/public/capture-lead/', views.capture_lead, name='capture_lead'),
    path('api/public/property-search/', views.property_search, name='property_search'),
]

