# Revolution Realty - SaaS-Enabled Admin Interface
# Multi-tenant admin with modern UX/UI inspired by leading platforms

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

# Import all models
from .models import *
from .saas_models import *

# ============================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================

class RevolutionAdminSite(admin.AdminSite):
    site_header = "Revolution Realty SaaS Platform"
    site_title = "Revolution Realty Admin"
    index_title = "Platform Management Dashboard"
    
    def index(self, request, extra_context=None):
        """Custom admin dashboard with SaaS metrics"""
        extra_context = extra_context or {}
        
        # SaaS Platform Metrics
        extra_context.update({
            'total_tenants': Tenant.objects.count(),
            'active_tenants': Tenant.objects.filter(status='active').count(),
            'trial_tenants': Tenant.objects.filter(status='trial').count(),
            'total_revenue': Invoice.objects.filter(status='paid').aggregate(
                total=Sum('total_amount')
            )['total'] or 0,
            'monthly_recurring_revenue': self.calculate_mrr(),
            'recent_signups': Tenant.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count(),
        })
        
        return super().index(request, extra_context)
    
    def calculate_mrr(self):
        """Calculate Monthly Recurring Revenue"""
        active_tenants = Tenant.objects.filter(status='active')
        mrr = sum(tenant.subscription_plan.monthly_price for tenant in active_tenants)
        return mrr

# Create custom admin site
admin_site = RevolutionAdminSite(name='revolution_admin')

# ============================================================================
# SAAS PLATFORM ADMIN
# ============================================================================

@admin.register(SubscriptionPlan, site=admin_site)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'monthly_price', 'max_agents', 'max_leads_per_month', 'is_active']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'plan_type', 'description')
        }),
        ('Pricing', {
            'fields': ('monthly_price', 'annual_price', 'setup_fee', 'transaction_fee_percentage')
        }),
        ('Limits', {
            'fields': ('max_agents', 'max_leads_per_month', 'max_properties', 'max_storage_gb')
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

@admin.register(Tenant, site=admin_site)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'subdomain', 'status', 'subscription_plan', 'current_agents', 'trial_status', 'created_at']
    list_filter = ['status', 'subscription_plan', 'created_at']
    search_fields = ['name', 'subdomain', 'domain', 'contact_email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'domain', 'subdomain')
        }),
        ('Contact', {
            'fields': ('owner', 'contact_email', 'contact_phone')
        }),
        ('Subscription', {
            'fields': ('subscription_plan', 'status', 'trial_ends_at', 'subscription_starts_at', 'next_billing_date')
        }),
        ('Usage Tracking', {
            'fields': ('current_agents', 'current_leads_this_month', 'current_properties', 'storage_used_gb'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def trial_status(self, obj):
        if obj.status == 'trial':
            if obj.is_trial_expired():
                return format_html('<span style="color: red;">Expired</span>')
            else:
                days_left = (obj.trial_ends_at - timezone.now()).days
                return format_html('<span style="color: orange;">{} days left</span>', days_left)
        return '-'
    trial_status.short_description = 'Trial Status'

@admin.register(TenantBranding, site=admin_site)
class TenantBrandingAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'site_title', 'primary_color', 'has_logo', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['tenant__name', 'site_title']
    
    fieldsets = (
        ('Tenant', {
            'fields': ('tenant',)
        }),
        ('Branding Assets', {
            'fields': ('logo', 'logo_dark', 'favicon', 'hero_image')
        }),
        ('Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'background_color', 'text_color')
        }),
        ('Typography', {
            'fields': ('font_family', 'heading_font')
        }),
        ('Content', {
            'fields': ('site_title', 'tagline', 'hero_title', 'hero_subtitle', 'about_text')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('SEO & Analytics', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id', 'facebook_pixel_id'),
            'classes': ('collapse',)
        }),
        ('Custom Code', {
            'fields': ('custom_css', 'custom_js'),
            'classes': ('collapse',)
        })
    )
    
    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True
    has_logo.short_description = 'Logo'

# ============================================================================
# LEAD MANAGEMENT ADMIN
# ============================================================================

@admin.register(LeadSource, site=admin_site)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost_per_lead', 'conversion_rate', 'lead_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    
    def lead_count(self, obj):
        return obj.lead_set.count()
    lead_count.short_description = 'Total Leads'

@admin.register(Lead, site=admin_site)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status', 'lead_type', 'assigned_agent', 'lead_score', 'created_at']
    list_filter = ['status', 'lead_type', 'source', 'assigned_agent', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_activity']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Lead Details', {
            'fields': ('status', 'lead_type', 'source', 'assigned_agent', 'lead_score')
        }),
        ('Property Preferences', {
            'fields': ('min_price', 'max_price', 'preferred_areas', 'bedrooms', 'bathrooms'),
            'classes': ('collapse',)
        }),
        ('Timeline', {
            'fields': ('next_followup', 'last_activity', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

# ============================================================================
# TRANSACTION MANAGEMENT ADMIN
# ============================================================================

@admin.register(Transaction, site=admin_site)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['property_address', 'lead', 'status', 'transaction_type', 'sale_price', 'estimated_commission', 'closing_date']
    list_filter = ['status', 'transaction_type', 'listing_agent', 'buyer_agent', 'created_at']
    search_fields = ['property_address', 'lead__first_name', 'lead__last_name']
    readonly_fields = ['id', 'estimated_commission', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('lead', 'property_address', 'status', 'transaction_type')
        }),
        ('Agents', {
            'fields': ('listing_agent', 'buyer_agent')
        }),
        ('Financial Details', {
            'fields': ('list_price', 'sale_price', 'commission_rate', 'estimated_commission')
        }),
        ('Important Dates', {
            'fields': ('contract_date', 'closing_date')
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# TASK MANAGEMENT ADMIN
# ============================================================================

@admin.register(TaskBoard, site=admin_site)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'team_member_count', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['team_members']
    
    def team_member_count(self, obj):
        return obj.team_members.count()
    team_member_count.short_description = 'Team Members'

@admin.register(Task, site=admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'priority', 'is_completed', 'due_date', 'created_by']
    list_filter = ['priority', 'is_completed', 'assigned_to', 'created_by', 'due_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'task_list', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Relationships', {
            'fields': ('lead', 'transaction'),
            'classes': ('collapse',)
        }),
        ('Status & Timing', {
            'fields': ('is_completed', 'due_date', 'completed_at', 'position')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# PROPERTY MANAGEMENT ADMIN
# ============================================================================

@admin.register(Property, site=admin_site)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'property_type', 'bedrooms', 'bathrooms', 'list_price', 'status', 'listing_agent']
    list_filter = ['status', 'property_type', 'city', 'listing_agent', 'listing_date']
    search_fields = ['address', 'city', 'mls_number', 'description']
    readonly_fields = ['id', 'view_count', 'favorite_count', 'inquiry_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('mls_number', 'address', 'city', 'state', 'zip_code')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built')
        }),
        ('Listing Information', {
            'fields': ('list_price', 'status', 'listing_agent', 'listing_date')
        }),
        ('Marketing', {
            'fields': ('description', 'features', 'virtual_tour_url'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'favorite_count', 'inquiry_count'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# ACTIVITY TRACKING ADMIN
# ============================================================================

@admin.register(Activity, site=admin_site)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'subject', 'lead', 'created_by', 'is_completed', 'created_at']
    list_filter = ['activity_type', 'is_completed', 'created_by', 'created_at']
    search_fields = ['subject', 'description', 'lead__first_name', 'lead__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('activity_type', 'subject', 'description')
        }),
        ('Relationships', {
            'fields': ('lead', 'transaction', 'property')
        }),
        ('Participants', {
            'fields': ('created_by', 'participants')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'completed_at', 'is_completed')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['participants']

# ============================================================================
# BILLING & ANALYTICS ADMIN
# ============================================================================

@admin.register(Invoice, site=admin_site)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'tenant', 'total_amount', 'status', 'issue_date', 'due_date']
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = ['invoice_number', 'tenant__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('tenant', 'invoice_number', 'status')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date')
        }),
        ('Payment', {
            'fields': ('payment_method', 'transaction_id'),
            'classes': ('collapse',)
        }),
        ('Line Items', {
            'fields': ('line_items',),
            'classes': ('collapse',)
        })
    )

@admin.register(UsageMetric, site=admin_site)
class UsageMetricAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'metric_type', 'value', 'period_start', 'period_end']
    list_filter = ['metric_type', 'period_start']
    search_fields = ['tenant__name']
    readonly_fields = ['created_at']

# ============================================================================
# SUPPORT & ONBOARDING ADMIN
# ============================================================================

@admin.register(SupportTicket, site=admin_site)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'tenant', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter = ['priority', 'status', 'assigned_to', 'created_at']
    search_fields = ['subject', 'description', 'tenant__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('tenant', 'created_by', 'subject', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('Timeline', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        })
    )

# ============================================================================
# ENHANCED USER ADMIN
# ============================================================================

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'tenant_count', 'last_login']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login']
    
    def tenant_count(self, obj):
        return obj.tenant_memberships.count()
    tenant_count.short_description = 'Tenants'

# Register the custom user admin
admin_site.register(User, CustomUserAdmin)

# ============================================================================
# REGISTER REMAINING MODELS
# ============================================================================

# Register other models with basic admin
models_to_register = [
    TaskList, PropertyImage, Feature, TenantFeature, Integration, 
    TenantIntegration, TenantAnalytics, OnboardingStep, TenantOnboarding,
    WebsiteTemplate, TenantTemplate, TenantUser
]

for model in models_to_register:
    admin_site.register(model)

# Also register legacy models
legacy_models = [
    Role, RoleUser, Activation, Persistence, Reminder, Throttle,
    DatAwards, DatProjects, DatProjectsImages, DatProjectsVideos,
    MailActivityLog, MailSignature, ContactsSearches, VendorRating,
    CommentReview, DatLikeReviews, UserBookmarkProject, RouteMatrix
]

for model in legacy_models:
    admin_site.register(model)

