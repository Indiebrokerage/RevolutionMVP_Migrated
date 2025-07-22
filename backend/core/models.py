# Revolution Realty - Enhanced Models
# Inspired by BoomTown, Commissions Inc, FollowUp Boss, Asana, Trello, Squarespace, Real Geeks, and Airbnb

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# ============================================================================
# LEAD MANAGEMENT (BoomTown + FollowUp Boss Inspired)
# ============================================================================

class LeadSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost_per_lead = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conversion_rate = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Lead(models.Model):
    LEAD_STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('nurturing', 'Nurturing'),
        ('hot', 'Hot Lead'),
        ('appointment', 'Appointment Set'),
        ('showing', 'Property Showing'),
        ('offer', 'Offer Made'),
        ('contract', 'Under Contract'),
        ('closed', 'Closed'),
        ('lost', 'Lost'),
        ('unqualified', 'Unqualified'),
    ]
    
    LEAD_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('investor', 'Investor'),
        ('renter', 'Renter'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Lead Details
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES, default='buyer')
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    
    # Scoring and Analytics (BoomTown Style)
    lead_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_activity = models.DateTimeField(auto_now=True)
    next_followup = models.DateTimeField(null=True, blank=True)
    
    # Property Preferences
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_areas = models.TextField(blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"

# ============================================================================
# TRANSACTION MANAGEMENT (Commissions Inc Inspired)
# ============================================================================

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('prospect', 'Prospect'),
        ('listing_agreement', 'Listing Agreement'),
        ('buyer_agreement', 'Buyer Agreement'),
        ('showing', 'Showing Properties'),
        ('offer_submitted', 'Offer Submitted'),
        ('negotiating', 'Negotiating'),
        ('under_contract', 'Under Contract'),
        ('inspection', 'Inspection Period'),
        ('appraisal', 'Appraisal'),
        ('financing', 'Financing'),
        ('final_walkthrough', 'Final Walkthrough'),
        ('closing', 'Closing'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('listing', 'Listing'),
        ('buyer_side', 'Buyer Side'),
        ('dual_agency', 'Dual Agency'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='transactions')
    property_address = models.CharField(max_length=255)
    
    # Transaction Details
    status = models.CharField(max_length=30, choices=TRANSACTION_STATUS_CHOICES, default='prospect')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='listing_transactions')
    buyer_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='buyer_transactions')
    
    # Financial Information
    list_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=3, default=0.06)  # 6%
    estimated_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Important Dates
    contract_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.sale_price and self.commission_rate:
            self.estimated_commission = self.sale_price * self.commission_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.property_address} - {self.get_status_display()}"

# ============================================================================
# TASK MANAGEMENT (Asana + Trello Inspired)
# ============================================================================

class TaskBoard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, related_name='task_boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TaskList(models.Model):
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name='task_lists')
    name = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.board.name} - {self.name}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    
    # Assignment and Priority
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Relationships
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status and Timing
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    position = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', '-created_at']
    
    def __str__(self):
        return self.title

# ============================================================================
# PROPERTY MANAGEMENT (Real Geeks + Airbnb Inspired)
# ============================================================================

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('single_family', 'Single Family Home'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('multi_family', 'Multi-Family'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
        ('investment', 'Investment Property'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('withdrawn', 'Withdrawn'),
        ('expired', 'Expired'),
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
    
    # Listing Information
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    listing_date = models.DateField(auto_now_add=True)
    
    # Marketing
    description = models.TextField(blank=True)
    features = models.TextField(blank=True)  # JSON field for amenities
    virtual_tour_url = models.URLField(blank=True)
    
    # Analytics (Airbnb Style)
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    inquiry_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.address}, {self.city} - ${self.list_price:,.0f}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['position']

# ============================================================================
# COMMUNICATION & ACTIVITY TRACKING (FollowUp Boss Inspired)
# ============================================================================

class Activity(models.Model):
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
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Relationships
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    
    # User Information
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participated_activities', blank=True)
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_activity_type_display()}: {self.subject}"

# ============================================================================
# SYSTEM SETTINGS (Squarespace Inspired)
# ============================================================================

class SiteSettings(models.Model):
    # Site Identity
    site_name = models.CharField(max_length=100, default="Revolution Realty")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site_assets/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site_assets/', null=True, blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # SEO Settings
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.TextField(blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Email Configuration
    smtp_host = models.CharField(max_length=100, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    
    # IDX Settings
    idx_provider = models.CharField(max_length=100, blank=True)
    idx_api_key = models.CharField(max_length=255, blank=True)
    idx_feed_url = models.URLField(blank=True)
    
    # Theme Settings
    primary_color = models.CharField(max_length=7, default="#3B82F6")  # Blue
    secondary_color = models.CharField(max_length=7, default="#10B981")  # Green
    accent_color = models.CharField(max_length=7, default="#F59E0B")  # Orange
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"

# ============================================================================
# LEGACY MODELS (From Original System)
# ============================================================================

# Sentinel Authentication Models
class Role(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    permissions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoleUser(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Activation(models.Model):
    user_id = models.IntegerField()
    code = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Persistence(models.Model):
    user_id = models.IntegerField()
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reminder(models.Model):
    user_id = models.IntegerField()
    code = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Throttle(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=255)
    ip = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Legacy Project Models
class DatAwards(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DatProjects(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DatProjectsImages(models.Model):
    project = models.ForeignKey(DatProjects, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class DatProjectsVideos(models.Model):
    project = models.ForeignKey(DatProjects, on_delete=models.CASCADE)
    video_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

# Communication Models
class MailActivityLog(models.Model):
    user_id = models.IntegerField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class MailSignature(models.Model):
    user_id = models.IntegerField()
    signature = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactsSearches(models.Model):
    user_id = models.IntegerField()
    search_term = models.CharField(max_length=255)
    results_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

# Review Models
class VendorRating(models.Model):
    vendor_name = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CommentReview(models.Model):
    user_id = models.IntegerField()
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

class DatLikeReviews(models.Model):
    user_id = models.IntegerField()
    review_id = models.IntegerField()
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Utility Models
class UserBookmarkProject(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class RouteMatrix(models.Model):
    route_name = models.CharField(max_length=255)
    permissions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Import all SaaS models to make them available to Django
from .saas_models import *

