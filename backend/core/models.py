# Revolution Realty - Complete Real Estate SaaS Platform Models
# Market-ready CRM with BoomTown, FollowUp Boss, Real Geeks, Commissions Inc features

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json

# Import all SaaS models
from .saas_models import *
from .crm_models import *

# ============================================================================
# CONTENT MANAGEMENT & WEBSITE BUILDER (SQUARESPACE-STYLE)
# ============================================================================

class WebsiteTemplate(models.Model):
    """Squarespace-style website templates"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('modern', 'Modern'),
        ('luxury', 'Luxury'),
        ('minimal', 'Minimal'),
        ('corporate', 'Corporate'),
        ('creative', 'Creative'),
    ])
    
    # Template files
    preview_image = models.ImageField(upload_to='templates/previews/', null=True, blank=True)
    template_data = models.JSONField(default=dict)  # Store template structure
    
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Website(models.Model):
    """Client websites built with the platform"""
    tenant = models.OneToOneField('Tenant', on_delete=models.CASCADE, related_name='website')
    template = models.ForeignKey(WebsiteTemplate, on_delete=models.SET_NULL, null=True)
    
    # Domain settings
    subdomain = models.CharField(max_length=100, unique=True)  # client.revolutionrealty.com
    custom_domain = models.CharField(max_length=200, blank=True)  # client.com
    
    # Branding
    logo = models.ImageField(upload_to='websites/logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#2563eb')  # Hex color
    secondary_color = models.CharField(max_length=7, default='#64748b')
    font_family = models.CharField(max_length=100, default='Inter')
    
    # Content
    site_title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    about_text = models.TextField(blank=True)
    contact_info = models.JSONField(default=dict)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Settings
    is_published = models.BooleanField(default=False)
    analytics_code = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.site_title} ({self.subdomain})"

class WebsitePage(models.Model):
    """Individual pages on client websites"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.JSONField(default=dict)  # Page builder content
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Settings
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['website', 'slug']
        ordering = ['order']
    
    def __str__(self):
        return f"{self.website.site_title} - {self.title}"

class LeadCaptureForm(models.Model):
    """Lead capture forms for websites"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='lead_forms')
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Form fields
    fields = models.JSONField(default=list)  # List of form fields
    
    # Settings
    redirect_url = models.URLField(blank=True)
    email_notifications = models.BooleanField(default=True)
    auto_responder = models.TextField(blank=True)
    
    # Analytics
    views = models.IntegerField(default=0)
    submissions = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def conversion_rate(self):
        if self.views > 0:
            return (self.submissions / self.views) * 100
        return 0
    
    def __str__(self):
        return f"{self.website.site_title} - {self.name}"

# ============================================================================
# EMAIL MARKETING & CAMPAIGNS
# ============================================================================

class EmailTemplate(models.Model):
    """Email templates for marketing campaigns"""
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    
    # Template type
    template_type = models.CharField(max_length=50, choices=[
        ('welcome', 'Welcome Email'),
        ('nurture', 'Lead Nurture'),
        ('listing_alert', 'New Listing Alert'),
        ('market_update', 'Market Update'),
        ('newsletter', 'Newsletter'),
        ('follow_up', 'Follow Up'),
        ('thank_you', 'Thank You'),
    ])
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class EmailCampaign(models.Model):
    """Email marketing campaigns"""
    name = models.CharField(max_length=200)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    
    # Recipients
    recipient_list = models.ManyToManyField(Lead, blank=True)
    recipient_criteria = models.JSONField(default=dict)  # Dynamic recipient selection
    
    # Scheduling
    send_date = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    
    # Analytics
    sent_count = models.IntegerField(default=0)
    opened_count = models.IntegerField(default=0)
    clicked_count = models.IntegerField(default=0)
    unsubscribed_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def open_rate(self):
        if self.sent_count > 0:
            return (self.opened_count / self.sent_count) * 100
        return 0
    
    def click_rate(self):
        if self.sent_count > 0:
            return (self.clicked_count / self.sent_count) * 100
        return 0
    
    def __str__(self):
        return self.name

# ============================================================================
# ANALYTICS & REPORTING
# ============================================================================

class AnalyticsEvent(models.Model):
    """Track user interactions and events"""
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('property_view', 'Property View'),
        ('lead_form_submit', 'Lead Form Submit'),
        ('email_open', 'Email Open'),
        ('email_click', 'Email Click'),
        ('search', 'Property Search'),
        ('contact_agent', 'Contact Agent'),
        ('schedule_showing', 'Schedule Showing'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    user_session = models.CharField(max_length=100)  # Session ID
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Event data
    page_url = models.URLField(blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    event_data = models.JSONField(default=dict)
    
    # Location data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event_type} - {self.created_at}"

class Report(models.Model):
    """Saved reports and dashboards"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    report_type = models.CharField(max_length=50, choices=[
        ('leads', 'Lead Report'),
        ('transactions', 'Transaction Report'),
        ('properties', 'Property Report'),
        ('marketing', 'Marketing Report'),
        ('financial', 'Financial Report'),
        ('custom', 'Custom Report'),
    ])
    
    # Report configuration
    filters = models.JSONField(default=dict)
    metrics = models.JSONField(default=list)
    chart_config = models.JSONField(default=dict)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_shared = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# ============================================================================
# INTEGRATIONS & API CONNECTIONS
# ============================================================================

class Integration(models.Model):
    """Third-party integrations"""
    name = models.CharField(max_length=100)
    integration_type = models.CharField(max_length=50, choices=[
        ('mls', 'MLS/IDX'),
        ('email', 'Email Service'),
        ('crm', 'CRM'),
        ('social', 'Social Media'),
        ('analytics', 'Analytics'),
        ('payment', 'Payment Processing'),
        ('document', 'Document Management'),
        ('calendar', 'Calendar'),
        ('communication', 'Communication'),
    ])
    
    description = models.TextField()
    api_endpoint = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    
    # Configuration
    config_fields = models.JSONField(default=list)  # Required configuration fields
    
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class TenantIntegration(models.Model):
    """Tenant-specific integration configurations"""
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, related_name='integrations')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    
    # Configuration data (encrypted)
    config_data = models.JSONField(default=dict)
    
    is_enabled = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['tenant', 'integration']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.integration.name}"

# ============================================================================
# NOTIFICATIONS & ALERTS
# ============================================================================

class Notification(models.Model):
    """In-app notifications"""
    NOTIFICATION_TYPES = [
        ('new_lead', 'New Lead'),
        ('lead_activity', 'Lead Activity'),
        ('task_due', 'Task Due'),
        ('appointment_reminder', 'Appointment Reminder'),
        ('contract_update', 'Contract Update'),
        ('system_alert', 'System Alert'),
        ('marketing_update', 'Marketing Update'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects
    related_lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    related_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"

# ============================================================================
# SYSTEM SETTINGS & CONFIGURATION
# ============================================================================

class SystemSetting(models.Model):
    """Global system settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    
    setting_type = models.CharField(max_length=50, choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ], default='string')
    
    is_public = models.BooleanField(default=False)  # Can be accessed by frontend
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"

# ============================================================================
# LEGACY MODELS (from original project)
# ============================================================================

# Keep existing models for backward compatibility
class DatProjects(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dat_projects'

class DatProjectsImages(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dat_projects_images'

class DatProjectsVideos(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    video_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dat_projects_videos'

class DatAwards(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dat_awards'

class DatLikeReviews(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dat_like_reviews'

class ContactsSearches(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts_searches'

class CommentReviews(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_reviews'

class Activations(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activations'

# Additional models for email functionality
class MailActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    activity_type = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mail_activity_logs'

class MailSignature(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mail_signatures'

# Features model for platform capabilities
class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    feature_key = models.CharField(max_length=50, unique=True)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Invoice model for billing
class Invoice(models.Model):
    INVOICE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, related_name='invoices')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.tenant.name}"

