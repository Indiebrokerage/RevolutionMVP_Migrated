# Revolution Realty - Comprehensive CRM Models
# Inspired by BoomTown, Commissions Inc, Real Geeks, FollowUp Boss, and modern CRM platforms

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json

# ============================================================================
# BOOMTOWN-STYLE LEAD MANAGEMENT & SCORING
# ============================================================================

class LeadSource(models.Model):
    """Lead sources with ROI tracking like BoomTown"""
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=50, choices=[
        ('website', 'Website'),
        ('facebook', 'Facebook Ads'),
        ('google', 'Google Ads'),
        ('zillow', 'Zillow'),
        ('realtor_com', 'Realtor.com'),
        ('referral', 'Referral'),
        ('open_house', 'Open House'),
        ('cold_call', 'Cold Call'),
        ('email', 'Email Campaign'),
        ('social_media', 'Social Media'),
        ('yard_sign', 'Yard Sign'),
        ('direct_mail', 'Direct Mail'),
        ('other', 'Other'),
    ])
    cost_per_lead = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    roi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.source_type})"

class Lead(models.Model):
    """BoomTown-style lead management with scoring"""
    LEAD_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('nurturing', 'Nurturing'),
        ('hot', 'Hot'),
        ('appointment_set', 'Appointment Set'),
        ('showing_scheduled', 'Showing Scheduled'),
        ('under_contract', 'Under Contract'),
        ('closed', 'Closed'),
        ('lost', 'Lost'),
        ('unresponsive', 'Unresponsive'),
    ]
    
    LEAD_TEMPERATURE = [
        ('cold', 'Cold'),
        ('warm', 'Warm'),
        ('hot', 'Hot'),
        ('burning', 'Burning'),
    ]
    
    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Lead Details
    source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    temperature = models.CharField(max_length=10, choices=LEAD_TEMPERATURE, default='cold')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # BoomTown-style Lead Scoring
    lead_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    engagement_score = models.IntegerField(default=0)
    website_visits = models.IntegerField(default=0)
    email_opens = models.IntegerField(default=0)
    email_clicks = models.IntegerField(default=0)
    property_views = models.IntegerField(default=0)
    search_activity = models.IntegerField(default=0)
    
    # Property Preferences
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_bedrooms = models.IntegerField(null=True, blank=True)
    preferred_bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    preferred_areas = models.JSONField(default=list)  # List of preferred neighborhoods/areas
    property_type = models.CharField(max_length=50, blank=True)
    
    # Timeline
    timeline = models.CharField(max_length=50, choices=[
        ('immediately', 'Immediately'),
        ('1_month', 'Within 1 Month'),
        ('3_months', '1-3 Months'),
        ('6_months', '3-6 Months'),
        ('1_year', '6-12 Months'),
        ('over_1_year', 'Over 1 Year'),
        ('just_looking', 'Just Looking'),
    ], blank=True)
    
    # Notes and Tags
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    next_followup = models.DateTimeField(null=True, blank=True)
    
    def calculate_lead_score(self):
        """BoomTown-style lead scoring algorithm"""
        score = 0
        
        # Engagement scoring
        score += min(self.website_visits * 2, 20)
        score += min(self.email_opens * 1, 15)
        score += min(self.email_clicks * 3, 20)
        score += min(self.property_views * 2, 25)
        score += min(self.search_activity * 1, 10)
        
        # Contact info completeness
        if self.phone:
            score += 10
        if self.email:
            score += 5
            
        # Property preferences completeness
        if self.min_price and self.max_price:
            score += 10
        if self.preferred_areas:
            score += 5
        if self.timeline and self.timeline != 'just_looking':
            score += 10
            
        self.lead_score = min(score, 100)
        return self.lead_score
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

# ============================================================================
# FOLLOWUP BOSS-STYLE ACTIVITY TRACKING & AUTOMATION
# ============================================================================

class Activity(models.Model):
    """FollowUp Boss-style activity tracking"""
    ACTIVITY_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('text', 'Text Message'),
        ('meeting', 'Meeting'),
        ('showing', 'Property Showing'),
        ('note', 'Note'),
        ('task', 'Task'),
        ('appointment', 'Appointment'),
        ('contract', 'Contract Activity'),
        ('closing', 'Closing Activity'),
    ]
    
    ACTIVITY_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    status = models.CharField(max_length=20, choices=ACTIVITY_STATUS, default='pending')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Scheduling
    scheduled_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    
    # Results
    outcome = models.TextField(blank=True)
    next_action = models.TextField(blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    # Automation
    is_automated = models.BooleanField(default=False)
    automation_trigger = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.activity_type} - {self.lead.first_name} {self.lead.last_name}"

class AutomationWorkflow(models.Model):
    """FollowUp Boss-style automation workflows"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Triggers
    trigger_type = models.CharField(max_length=50, choices=[
        ('new_lead', 'New Lead'),
        ('lead_status_change', 'Lead Status Change'),
        ('no_activity', 'No Activity for X Days'),
        ('property_view', 'Property View'),
        ('email_open', 'Email Open'),
        ('website_visit', 'Website Visit'),
        ('form_submission', 'Form Submission'),
    ])
    trigger_conditions = models.JSONField(default=dict)
    
    # Actions
    actions = models.JSONField(default=list)  # List of actions to perform
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# ============================================================================
# COMMISSIONS INC-STYLE TRANSACTION MANAGEMENT
# ============================================================================

class Transaction(models.Model):
    """Commissions Inc-style transaction tracking"""
    TRANSACTION_TYPES = [
        ('listing', 'Listing'),
        ('buyer', 'Buyer'),
        ('dual', 'Dual Agency'),
        ('referral_out', 'Referral Out'),
        ('referral_in', 'Referral In'),
    ]
    
    TRANSACTION_STATUS = [
        ('prospect', 'Prospect'),
        ('active', 'Active'),
        ('under_contract', 'Under Contract'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    # Basic Info
    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='prospect')
    
    # Parties
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listing_transactions')
    buyer_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer_transactions')
    
    # Property Info
    property_address = models.CharField(max_length=300)
    property_city = models.CharField(max_length=100)
    property_state = models.CharField(max_length=50)
    property_zip = models.CharField(max_length=20)
    
    # Financial Details
    list_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=3, default=0.06)  # 6% = 0.06
    gross_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Commission Splits
    listing_side_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    buyer_side_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agent_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    brokerage_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Important Dates
    listing_date = models.DateField(null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_commissions(self):
        """Calculate commission splits"""
        if self.sale_price and self.commission_rate:
            self.gross_commission = self.sale_price * self.commission_rate
            
            # Default 50/50 split between listing and buyer sides
            self.listing_side_commission = self.gross_commission / 2
            self.buyer_side_commission = self.gross_commission / 2
            
            # Agent gets 70% by default (configurable)
            agent_split = 0.70
            self.agent_commission = self.gross_commission * agent_split
            self.brokerage_commission = self.gross_commission * (1 - agent_split)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.property_address}"

class CommissionSplit(models.Model):
    """Detailed commission split tracking"""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='commission_splits')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    
    split_type = models.CharField(max_length=50, choices=[
        ('listing_agent', 'Listing Agent'),
        ('buyer_agent', 'Buyer Agent'),
        ('referral_fee', 'Referral Fee'),
        ('team_lead', 'Team Lead'),
        ('mentor', 'Mentor'),
        ('brokerage', 'Brokerage'),
    ])
    
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # 70.00 = 70%
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.agent.get_full_name()} - {self.percentage}% - ${self.amount}"

# ============================================================================
# REAL GEEKS-STYLE PROPERTY MANAGEMENT
# ============================================================================

class Property(models.Model):
    """Real Geeks-style property management"""
    PROPERTY_TYPES = [
        ('single_family', 'Single Family Home'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('multi_family', 'Multi-Family'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
        ('investment', 'Investment Property'),
    ]
    
    PROPERTY_STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('off_market', 'Off Market'),
        ('coming_soon', 'Coming Soon'),
    ]
    
    # Basic Info
    mls_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    
    # Property Details
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='active')
    
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_feet = models.IntegerField(null=True, blank=True)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    
    # Pricing
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Features
    features = models.JSONField(default=list)  # Pool, garage, etc.
    amenities = models.JSONField(default=list)
    
    # Listing Info
    listing_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    listing_date = models.DateField(null=True, blank=True)
    days_on_market = models.IntegerField(default=0)
    
    # SEO and Marketing
    description = models.TextField(blank=True)
    virtual_tour_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Analytics
    view_count = models.IntegerField(default=0)
    lead_count = models.IntegerField(default=0)
    showing_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_price_per_sqft(self):
        if self.square_feet and self.list_price:
            self.price_per_sqft = self.list_price / self.square_feet
    
    def __str__(self):
        return f"{self.address}, {self.city} - ${self.list_price:,.0f}"

class PropertyImage(models.Model):
    """Property photos and media"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']

# ============================================================================
# TASK MANAGEMENT (ASANA/TRELLO-STYLE)
# ============================================================================

class TaskBoard(models.Model):
    """Kanban-style task boards"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='task_boards', blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TaskList(models.Model):
    """Task list columns (To Do, In Progress, Done)"""
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name='task_lists')
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.board.name} - {self.name}"

class Task(models.Model):
    """Individual tasks"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Relationships
    related_lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    related_transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    related_property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title

