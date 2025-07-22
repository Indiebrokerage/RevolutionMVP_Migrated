# Revolution Realty - API Serializers
# For frontend integration and REST API endpoints

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Lead, LeadSource, Transaction, Task, TaskBoard, TaskList,
    Property, PropertyImage, Activity, SiteSettings
)

# ============================================================================
# USER SERIALIZERS
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_staff']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

# ============================================================================
# LEAD MANAGEMENT SERIALIZERS
# ============================================================================

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSource
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    assigned_agent_name = serializers.CharField(source='assigned_agent.get_full_name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    lead_type_display = serializers.CharField(source='get_lead_type_display', read_only=True)
    days_since_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Lead
        fields = '__all__'
    
    def get_days_since_created(self, obj):
        from django.utils import timezone
        return (timezone.now() - obj.created_at).days

class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'lead_type',
            'source', 'min_price', 'max_price', 'preferred_areas',
            'bedrooms', 'bathrooms'
        ]

# ============================================================================
# TRANSACTION SERIALIZERS
# ============================================================================

class TransactionSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.first_name', read_only=True)
    listing_agent_name = serializers.CharField(source='listing_agent.get_full_name', read_only=True)
    buyer_agent_name = serializers.CharField(source='buyer_agent.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    days_to_closing = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = '__all__'
    
    def get_days_to_closing(self, obj):
        if obj.closing_date:
            from django.utils import timezone
            return (obj.closing_date - timezone.now().date()).days
        return None

# ============================================================================
# TASK MANAGEMENT SERIALIZERS
# ============================================================================

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    lead_name = serializers.CharField(source='lead.first_name', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = '__all__'
    
    def get_is_overdue(self, obj):
        if obj.due_date and not obj.is_completed:
            from django.utils import timezone
            return obj.due_date < timezone.now()
        return False

class TaskListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskList
        fields = '__all__'
    
    def get_task_count(self, obj):
        return obj.tasks.count()

class TaskBoardSerializer(serializers.ModelSerializer):
    task_lists = TaskListSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    team_members_names = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskBoard
        fields = '__all__'
    
    def get_team_members_names(self, obj):
        return [member.get_full_name() for member in obj.team_members.all()]

# ============================================================================
# PROPERTY SERIALIZERS
# ============================================================================

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    listing_agent_name = serializers.CharField(source='listing_agent.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    full_address = serializers.SerializerMethodField()
    price_per_sqft = serializers.SerializerMethodField()
    days_on_market = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = '__all__'
    
    def get_full_address(self, obj):
        return f"{obj.address}, {obj.city}, {obj.state} {obj.zip_code}"
    
    def get_price_per_sqft(self, obj):
        if obj.square_feet and obj.square_feet > 0:
            return round(float(obj.list_price) / obj.square_feet, 2)
        return None
    
    def get_days_on_market(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.listing_date).days

class PropertyListSerializer(serializers.ModelSerializer):
    """Simplified serializer for property lists"""
    primary_image = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'address', 'city', 'state', 'zip_code', 'full_address',
            'property_type', 'bedrooms', 'bathrooms', 'square_feet',
            'list_price', 'status', 'primary_image', 'listing_date'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None
    
    def get_full_address(self, obj):
        return f"{obj.address}, {obj.city}, {obj.state} {obj.zip_code}"

# ============================================================================
# ACTIVITY SERIALIZERS
# ============================================================================

class ActivitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    lead_name = serializers.CharField(source='lead.first_name', read_only=True)
    property_address = serializers.CharField(source='property.address', read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'

# ============================================================================
# SITE SETTINGS SERIALIZERS
# ============================================================================

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

# ============================================================================
# DASHBOARD ANALYTICS SERIALIZERS
# ============================================================================

class DashboardStatsSerializer(serializers.Serializer):
    """Custom serializer for dashboard statistics"""
    total_leads = serializers.IntegerField()
    new_leads_today = serializers.IntegerField()
    hot_leads = serializers.IntegerField()
    total_transactions = serializers.IntegerField()
    active_transactions = serializers.IntegerField()
    closed_transactions_this_month = serializers.IntegerField()
    total_properties = serializers.IntegerField()
    active_listings = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    total_commission_this_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    conversion_rate = serializers.FloatField()

class LeadSourceStatsSerializer(serializers.Serializer):
    """Lead source performance statistics"""
    source_name = serializers.CharField()
    lead_count = serializers.IntegerField()
    conversion_rate = serializers.FloatField()
    cost_per_lead = serializers.DecimalField(max_digits=10, decimal_places=2)

class MonthlyStatsSerializer(serializers.Serializer):
    """Monthly performance statistics"""
    month = serializers.CharField()
    leads = serializers.IntegerField()
    transactions = serializers.IntegerField()
    commission = serializers.DecimalField(max_digits=12, decimal_places=2)

