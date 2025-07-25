# Revolution Realty - Admin Configuration
# Market-ready CRM admin interface

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .saas_models import *

# ============================================================================
# CUSTOM ADMIN SITE
# ============================================================================

class RevolutionAdminSite(admin.AdminSite):
    site_header = "Revolution Realty Administration"
    site_title = "Revolution Realty Admin"
    index_title = "Platform Management Dashboard"
    
    def get_app_list(self, request, app_label=None):
        """Customize admin app list organization"""
        app_list = super().get_app_list(request, app_label)
        
        # Custom organization of models
        custom_order = {
            'Core': ['Lead', 'Property', 'Transaction', 'Task', 'Activity'],
            'SaaS Management': ['Tenant', 'SubscriptionPlan', 'Invoice'],
            'System': ['User', 'SiteSettings'],
        }
        
        return app_list

# Create custom admin site instance
admin_site = RevolutionAdminSite(name='revolution_admin')

# ============================================================================
# LEAD MANAGEMENT ADMIN
# ============================================================================

@admin.register(LeadSource, site=admin_site)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost_per_lead', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

@admin.register(Lead, site=admin_site)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status', 'lead_score', 'source', 'assigned_agent', 'created_at']
    list_filter = ['status', 'lead_type', 'source', 'assigned_agent', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Lead Details', {
            'fields': ('status', 'lead_type', 'source', 'assigned_agent')
        }),
        ('Scoring & Engagement', {
            'fields': ('lead_score', 'engagement_score', 'website_visits', 'email_opens', 'email_clicks')
        }),
        ('Property Preferences', {
            'fields': ('min_price', 'max_price', 'preferred_bedrooms', 'preferred_bathrooms', 'preferred_locations')
        }),
        ('Notes & Timestamps', {
            'fields': ('notes', 'last_contact', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

# ============================================================================
# PROPERTY MANAGEMENT ADMIN
# ============================================================================

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ['image', 'caption', 'order', 'is_primary']

@admin.register(Property, site=admin_site)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'property_type', 'bedrooms', 'bathrooms', 'list_price', 'status', 'days_on_market', 'listing_agent']
    list_filter = ['status', 'property_type', 'city', 'listing_agent', 'created_at']
    search_fields = ['address', 'city', 'mls_number']
    ordering = ['-created_at']
    readonly_fields = ['id', 'days_on_market', 'view_count', 'favorite_count', 'lead_count', 'created_at', 'updated_at']
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('mls_number', 'address', 'city', 'state', 'zip_code')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built')
        }),
        ('Pricing', {
            'fields': ('list_price', 'original_price', 'price_per_sqft')
        }),
        ('Status & Dates', {
            'fields': ('status', 'list_date', 'days_on_market')
        }),
        ('Agent & Description', {
            'fields': ('listing_agent', 'description', 'features')
        }),
        ('Analytics', {
            'fields': ('view_count', 'favorite_count', 'lead_count', 'showing_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# TRANSACTION MANAGEMENT ADMIN
# ============================================================================

@admin.register(Transaction, site=admin_site)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['property_address', 'transaction_type', 'status', 'sale_price', 'estimated_commission', 'listing_agent', 'buyer_agent', 'expected_close_date']
    list_filter = ['status', 'transaction_type', 'listing_agent', 'buyer_agent', 'created_at']
    search_fields = ['property__address', 'property__city']
    ordering = ['-created_at']
    readonly_fields = ['id', 'estimated_commission', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('property', 'lead', 'transaction_type', 'status')
        }),
        ('Agents', {
            'fields': ('listing_agent', 'buyer_agent')
        }),
        ('Financial Information', {
            'fields': ('sale_price', 'commission_rate', 'estimated_commission', 'actual_commission')
        }),
        ('Important Dates', {
            'fields': ('contract_date', 'expected_close_date', 'actual_close_date')
        }),
        ('Notes & Timestamps', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def property_address(self, obj):
        return obj.property.address
    property_address.short_description = 'Property'

# ============================================================================
# TASK MANAGEMENT ADMIN
# ============================================================================

@admin.register(TaskBoard, site=admin_site)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ['title', 'assigned_to', 'priority', 'due_date', 'is_completed']

@admin.register(TaskList, site=admin_site)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ['name', 'board', 'position', 'created_at']
    list_filter = ['board', 'created_at']
    search_fields = ['name', 'board__name']
    ordering = ['board', 'position']
    inlines = [TaskInline]

@admin.register(Task, site=admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_list', 'assigned_to', 'priority', 'due_date', 'is_completed', 'created_by']
    list_filter = ['priority', 'is_completed', 'assigned_to', 'created_by', 'due_date']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('task_list', 'title', 'description')
        }),
        ('Assignment & Priority', {
            'fields': ('assigned_to', 'created_by', 'priority')
        }),
        ('Status & Dates', {
            'fields': ('is_completed', 'due_date', 'completed_at')
        }),
        ('Organization', {
            'fields': ('position', 'tags')
        }),
        ('Related Objects', {
            'fields': ('lead', 'property', 'transaction'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# ACTIVITY TRACKING ADMIN
# ============================================================================

@admin.register(Activity, site=admin_site)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['subject', 'activity_type', 'lead', 'created_by', 'scheduled_at', 'is_completed', 'created_at']
    list_filter = ['activity_type', 'is_completed', 'created_by', 'created_at']
    search_fields = ['subject', 'description', 'lead__first_name', 'lead__last_name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('activity_type', 'subject', 'description')
        }),
        ('Related Objects', {
            'fields': ('lead', 'property', 'transaction')
        }),
        ('User & Timing', {
            'fields': ('created_by', 'scheduled_at', 'completed_at', 'is_completed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# SAAS MANAGEMENT ADMIN
# ============================================================================

@admin.register(SubscriptionPlan, site=admin_site)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'monthly_price', 'max_agents', 'max_leads_per_month', 'is_active']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['monthly_price']

@admin.register(Tenant, site=admin_site)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'subscription_plan', 'status', 'created_at', 'next_billing_date']
    list_filter = ['status', 'subscription_plan', 'created_at']
    search_fields = ['name', 'domain', 'contact_email']
    ordering = ['-created_at']

@admin.register(Feature, site=admin_site)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Integration, site=admin_site)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'is_active']
    list_filter = ['provider', 'is_active']
    search_fields = ['name', 'description']

@admin.register(WebsiteTemplate, site=admin_site)
class WebsiteTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

# ============================================================================
# SYSTEM ADMIN
# ============================================================================

@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Information', {
            'fields': ('site_name', 'tagline', 'phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url')
        }),
        ('Branding', {
            'fields': ('logo', 'primary_color', 'secondary_color', 'accent_color')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Features', {
            'fields': ('enable_idx_integration', 'enable_lead_capture', 'enable_virtual_tours')
        })
    )

# Register User model with custom admin site
admin_site.register(User, UserAdmin)

