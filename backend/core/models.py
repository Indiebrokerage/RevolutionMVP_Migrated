# Market-ready CRM with BoomTown, FollowUp Boss, Real Geeks, Commissions Inc features

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json

# ============================================================================
# LEAD MANAGEMENT (BOOMTOWN-STYLE)
# ============================================================================

class LeadSource(models.Model):
    """Lead source tracking for ROI analysis"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost_per_lead = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Lead(models.Model):
    """BoomTown-style lead management with scoring"""
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('hot', 'Hot'),
        ('appointment', 'Appointment Set'),
        ('nurturing', 'Nurturing'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    LEAD_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('both', 'Both'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Lead Details
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    lead_type = models.CharField(max_length=10, choices=LEAD_TYPE_CHOICES, default='buyer')
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    
    # BoomTown-style scoring
    lead_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    engagement_score = models.IntegerField(default=0)
    website_visits = models.IntegerField(default=0)
    email_opens = models.IntegerField(default=0)
    email_clicks = models.IntegerField(default=0)
    
    # Property Preferences
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_bedrooms = models.IntegerField(null=True, blank=True)
    preferred_bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    preferred_locations = models.TextField(blank=True)
    
    # Assignment & Notes
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"

# ============================================================================
# PROPERTY MANAGEMENT (REAL GEEKS-STYLE)
# ============================================================================

class Property(models.Model):
    """Real Geeks-style property management"""
    PROPERTY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('withdrawn', 'Withdrawn'),
        ('expired', 'Expired'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('single_family', 'Single Family'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('multi_family', 'Multi-Family'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mls_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    # Property Details
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_feet = models.IntegerField(null=True, blank=True)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    
    # Pricing
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Status & Dates
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES, default='active')
    list_date = models.DateField()
    days_on_market = models.IntegerField(default=0)
    
    # Agent Information
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='listed_properties')
    
    # Description & Features
    description = models.TextField(blank=True)
    features = models.JSONField(default=dict)  # Store property features as JSON
    
    # Analytics (Real Geeks-style)
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    lead_count = models.IntegerField(default=0)
    showing_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.address}, {self.city} - ${self.list_price:,.0f}"

class PropertyImage(models.Model):
    """Property images with ordering"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']

# ============================================================================
# TRANSACTION MANAGEMENT (COMMISSIONS INC-STYLE)
# ============================================================================

class Transaction(models.Model):
    """Commissions Inc-style transaction tracking"""
    TRANSACTION_STATUS_CHOICES = [
        ('prospect', 'Prospect'),
        ('under_contract', 'Under Contract'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('listing', 'Listing'),
        ('buyer', 'Buyer'),
        ('dual', 'Dual Agency'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Transaction Details
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='prospect')
    
    # Agents
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='listing_transactions')
    buyer_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_transactions')
    
    # Financial Information
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=3, default=0.06)  # 6% = 0.06
    estimated_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Important Dates
    contract_date = models.DateField(null=True, blank=True)
    expected_close_date = models.DateField(null=True, blank=True)
    actual_close_date = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate estimated commission
        if self.sale_price and self.commission_rate:
            self.estimated_commission = self.sale_price * self.commission_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.property.address} - {self.get_status_display()}"

# ============================================================================
# TASK MANAGEMENT (ASANA/TRELLO-STYLE)
# ============================================================================

class TaskBoard(models.Model):
    """Asana/Trello-style task boards"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TaskList(models.Model):
    """Task lists within boards (like Trello columns)"""
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position', 'created_at']
    
    def __str__(self):
        return f"{self.board.name} - {self.name}"

class Task(models.Model):
    """Individual tasks with Asana-style features"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Assignment & Priority
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Status & Dates
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Organization
    position = models.IntegerField(default=0)
    tags = models.JSONField(default=list)  # Store tags as JSON array
    
    # Related Objects
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', '-created_at']
    
    def __str__(self):
        return self.title

# ============================================================================
# ACTIVITY TRACKING (FOLLOWUP BOSS-STYLE)
# ============================================================================

class Activity(models.Model):
    """FollowUp Boss-style activity tracking"""
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('text', 'Text Message'),
        ('meeting', 'Meeting'),
        ('showing', 'Property Showing'),
        ('note', 'Note'),
        ('task', 'Task'),
        ('document', 'Document'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Related Objects
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    # User & Timing
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_activity_type_display()}: {self.subject}"

# ============================================================================
# SITE SETTINGS & CONFIGURATION
# ============================================================================

class SiteSettings(models.Model):
    """Global site settings"""
    # Company Information
    site_name = models.CharField(max_length=100, default="Revolution Realty")
    tagline = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='branding/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#3B82F6")  # Blue
    secondary_color = models.CharField(max_length=7, default="#1F2937")  # Dark Gray
    accent_color = models.CharField(max_length=7, default="#10B981")  # Green
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Features
    enable_idx_integration = models.BooleanField(default=True)
    enable_lead_capture = models.BooleanField(default=True)
    enable_virtual_tours = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name

