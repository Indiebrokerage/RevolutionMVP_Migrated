# Revolution Realty - SaaS & Multi-Tenant Models
# White-label real estate platform architecture

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json

# ============================================================================
# SAAS & TENANT MANAGEMENT
# ============================================================================

class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_fee_percentage = models.DecimalField(max_digits=5, decimal_places=3, default=0)  # 0.5% = 0.005
    
    # Limits
    max_agents = models.IntegerField(default=1)
    max_leads_per_month = models.IntegerField(default=100)
    max_properties = models.IntegerField(default=50)
    max_storage_gb = models.IntegerField(default=1)  # Storage in GB
    
    # Features
    features = models.JSONField(default=dict)  # Store feature flags as JSON
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ${self.monthly_price}/month"

class Tenant(models.Model):
    """Multi-tenant organization model"""
    TENANT_STATUS = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)  # "Smith Realty Group"
    slug = models.SlugField(unique=True)  # "smith-realty-group"
    domain = models.CharField(max_length=100, unique=True)  # "smithrealty.com"
    subdomain = models.CharField(max_length=50, unique=True)  # "smith" -> smith.revolutionrealty.com
    
    # Contact Information
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tenants')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Subscription
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=TENANT_STATUS, default='trial')
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_starts_at = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)
    
    # Usage Tracking
    current_agents = models.IntegerField(default=0)
    current_leads_this_month = models.IntegerField(default=0)
    current_properties = models.IntegerField(default=0)
    storage_used_gb = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def is_trial_expired(self):
        if self.trial_ends_at:
            return timezone.now() > self.trial_ends_at
        return False
    
    def can_add_agent(self):
        return self.current_agents < self.subscription_plan.max_agents
    
    def can_add_lead(self):
        return self.current_leads_this_month < self.subscription_plan.max_leads_per_month
    
    def can_add_property(self):
        return self.current_properties < self.subscription_plan.max_properties

class TenantUser(models.Model):
    """Link users to tenants with roles"""
    USER_ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('agent', 'Agent'),
        ('assistant', 'Assistant'),
        ('viewer', 'Viewer'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_memberships')
    role = models.CharField(max_length=20, choices=USER_ROLES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tenant', 'user']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.tenant.name} ({self.role})"

# ============================================================================
# WHITE-LABEL BRANDING & CUSTOMIZATION
# ============================================================================

class TenantBranding(models.Model):
    """White-label branding configuration per tenant"""
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='branding')
    
    # Logo & Images
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    logo_dark = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)  # For dark themes
    favicon = models.ImageField(upload_to='tenant_favicons/', null=True, blank=True)
    hero_image = models.ImageField(upload_to='tenant_heroes/', null=True, blank=True)
    
    # Colors (Hex codes)
    primary_color = models.CharField(max_length=7, default="#3B82F6")  # Blue
    secondary_color = models.CharField(max_length=7, default="#10B981")  # Green
    accent_color = models.CharField(max_length=7, default="#F59E0B")  # Orange
    background_color = models.CharField(max_length=7, default="#FFFFFF")  # White
    text_color = models.CharField(max_length=7, default="#1F2937")  # Dark gray
    
    # Typography
    font_family = models.CharField(max_length=100, default="Inter, sans-serif")
    heading_font = models.CharField(max_length=100, blank=True)  # Optional separate heading font
    
    # Website Content
    site_title = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.TextField(blank=True)
    about_text = models.TextField(blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.TextField(blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    # Custom CSS/JS
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Branding for {self.tenant.name}"

class WebsiteTemplate(models.Model):
    """Available website templates for tenants"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='template_previews/')
    template_files = models.JSONField()  # Store template file paths/configuration
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TenantTemplate(models.Model):
    """Template selection per tenant"""
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='template')
    template = models.ForeignKey(WebsiteTemplate, on_delete=models.CASCADE)
    customizations = models.JSONField(default=dict)  # Store template-specific customizations
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tenant.name} - {self.template.name}"

# ============================================================================
# BILLING & PAYMENTS
# ============================================================================

class Invoice(models.Model):
    INVOICE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dates
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    
    # Payment Details
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Line Items (stored as JSON for flexibility)
    line_items = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.tenant.name}"

class UsageMetric(models.Model):
    """Track usage metrics for billing"""
    METRIC_TYPES = [
        ('leads', 'Leads'),
        ('transactions', 'Transactions'),
        ('storage', 'Storage'),
        ('api_calls', 'API Calls'),
        ('emails_sent', 'Emails Sent'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='usage_metrics')
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tenant', 'metric_type', 'period_start']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.metric_type}: {self.value}"

# ============================================================================
# FEATURE FLAGS & PERMISSIONS
# ============================================================================

class Feature(models.Model):
    """Available features in the platform"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    feature_key = models.CharField(max_length=50, unique=True)  # Used in code
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TenantFeature(models.Model):
    """Feature access per tenant"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    usage_limit = models.IntegerField(null=True, blank=True)  # Optional usage limit
    current_usage = models.IntegerField(default=0)
    enabled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tenant', 'feature']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.feature.name}"
    
    def can_use_feature(self):
        if not self.is_enabled:
            return False
        if self.usage_limit and self.current_usage >= self.usage_limit:
            return False
        return True

# ============================================================================
# INTEGRATION & API MANAGEMENT
# ============================================================================

class Integration(models.Model):
    """Available third-party integrations"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    provider = models.CharField(max_length=100)  # "Zapier", "MLS", "Mailchimp", etc.
    integration_type = models.CharField(max_length=50)  # "crm", "email", "mls", "payment"
    logo = models.ImageField(upload_to='integration_logos/', null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    setup_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class TenantIntegration(models.Model):
    """Integration configurations per tenant"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='integrations')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)  # Store API keys, settings, etc.
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['tenant', 'integration']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.integration.name}"

# ============================================================================
# ANALYTICS & REPORTING
# ============================================================================

class TenantAnalytics(models.Model):
    """Analytics data per tenant"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='analytics')
    
    # Website Analytics
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    bounce_rate = models.FloatField(default=0)
    avg_session_duration = models.IntegerField(default=0)  # in seconds
    
    # Lead Analytics
    leads_generated = models.IntegerField(default=0)
    leads_converted = models.IntegerField(default=0)
    conversion_rate = models.FloatField(default=0)
    
    # Transaction Analytics
    transactions_closed = models.IntegerField(default=0)
    total_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    avg_days_to_close = models.IntegerField(default=0)
    
    # Period
    period_start = models.DateField()
    period_end = models.DateField()
    period_type = models.CharField(max_length=20)  # 'daily', 'weekly', 'monthly'
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tenant', 'period_start', 'period_type']
    
    def __str__(self):
        return f"{self.tenant.name} Analytics - {self.period_start}"

# ============================================================================
# SUPPORT & ONBOARDING
# ============================================================================

class SupportTicket(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting', 'Waiting for Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='support_tickets')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"

class OnboardingStep(models.Model):
    """Onboarding checklist for new tenants"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField()
    is_required = models.BooleanField(default=True)
    help_text = models.TextField(blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class TenantOnboarding(models.Model):
    """Track onboarding progress per tenant"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='onboarding_progress')
    step = models.ForeignKey(OnboardingStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['tenant', 'step']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.step.name}"

