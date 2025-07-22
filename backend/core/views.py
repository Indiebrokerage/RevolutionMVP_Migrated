# Revolution Realty - API Views
# Comprehensive REST API for frontend integration

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (
    Lead, LeadSource, Transaction, Task, TaskBoard, TaskList,
    Property, PropertyImage, Activity, SiteSettings
)
from .serializers import (
    LeadSerializer, LeadCreateSerializer, LeadSourceSerializer,
    TransactionSerializer, TaskSerializer, TaskBoardSerializer, TaskListSerializer,
    PropertySerializer, PropertyListSerializer, PropertyImageSerializer,
    ActivitySerializer, SiteSettingsSerializer, UserSerializer,
    DashboardStatsSerializer, LeadSourceStatsSerializer, MonthlyStatsSerializer
)

# ============================================================================
# FRONTEND VIEWS (React Integration)
# ============================================================================

def home_view(request):
    """Serve React frontend"""
    return render(request, 'index.html')

@api_view(['GET'])
@permission_classes([AllowAny])
def api_welcome(request):
    """API welcome endpoint"""
    return Response({
        'message': 'Welcome to Revolution Realty API',
        'version': '2.0',
        'endpoints': {
            'leads': '/api/leads/',
            'transactions': '/api/transactions/',
            'properties': '/api/properties/',
            'tasks': '/api/tasks/',
            'dashboard': '/api/dashboard/',
        }
    })

# ============================================================================
# DASHBOARD & ANALYTICS VIEWS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Comprehensive dashboard statistics"""
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    
    # Lead Statistics
    total_leads = Lead.objects.count()
    new_leads_today = Lead.objects.filter(created_at__date=today).count()
    hot_leads = Lead.objects.filter(status='hot').count()
    
    # Transaction Statistics
    total_transactions = Transaction.objects.count()
    active_transactions = Transaction.objects.exclude(status__in=['closed', 'cancelled']).count()
    closed_transactions_this_month = Transaction.objects.filter(
        status='closed',
        updated_at__date__gte=this_month_start
    ).count()
    
    # Property Statistics
    total_properties = Property.objects.count()
    active_listings = Property.objects.filter(status='active').count()
    
    # Task Statistics
    pending_tasks = Task.objects.filter(is_completed=False).count()
    overdue_tasks = Task.objects.filter(
        is_completed=False,
        due_date__lt=timezone.now()
    ).count()
    
    # Financial Statistics
    total_commission_this_month = Transaction.objects.filter(
        status='closed',
        updated_at__date__gte=this_month_start
    ).aggregate(total=Sum('estimated_commission'))['total'] or 0
    
    # Conversion Rate
    qualified_leads = Lead.objects.filter(status__in=['qualified', 'hot', 'appointment']).count()
    conversion_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
    
    stats = {
        'total_leads': total_leads,
        'new_leads_today': new_leads_today,
        'hot_leads': hot_leads,
        'total_transactions': total_transactions,
        'active_transactions': active_transactions,
        'closed_transactions_this_month': closed_transactions_this_month,
        'total_properties': total_properties,
        'active_listings': active_listings,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'total_commission_this_month': total_commission_this_month,
        'conversion_rate': round(conversion_rate, 2)
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lead_source_performance(request):
    """Lead source performance analytics"""
    sources = LeadSource.objects.annotate(
        lead_count=Count('lead')
    ).filter(lead_count__gt=0)
    
    stats = []
    for source in sources:
        qualified_leads = source.lead_set.filter(status__in=['qualified', 'hot', 'appointment']).count()
        conversion_rate = (qualified_leads / source.lead_count * 100) if source.lead_count > 0 else 0
        
        stats.append({
            'source_name': source.name,
            'lead_count': source.lead_count,
            'conversion_rate': round(conversion_rate, 2),
            'cost_per_lead': source.cost_per_lead
        })
    
    serializer = LeadSourceStatsSerializer(stats, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_performance(request):
    """Monthly performance trends"""
    # Get last 12 months of data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    
    monthly_stats = []
    current_date = start_date.replace(day=1)
    
    while current_date <= end_date:
        next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        leads_count = Lead.objects.filter(
            created_at__date__gte=current_date,
            created_at__date__lt=next_month
        ).count()
        
        transactions_count = Transaction.objects.filter(
            created_at__date__gte=current_date,
            created_at__date__lt=next_month
        ).count()
        
        commission = Transaction.objects.filter(
            status='closed',
            updated_at__date__gte=current_date,
            updated_at__date__lt=next_month
        ).aggregate(total=Sum('estimated_commission'))['total'] or 0
        
        monthly_stats.append({
            'month': current_date.strftime('%Y-%m'),
            'leads': leads_count,
            'transactions': transactions_count,
            'commission': commission
        })
        
        current_date = next_month
    
    serializer = MonthlyStatsSerializer(monthly_stats, many=True)
    return Response(serializer.data)

# ============================================================================
# LEAD MANAGEMENT VIEWSETS
# ============================================================================

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LeadCreateSerializer
        return LeadSerializer
    
    def get_queryset(self):
        queryset = Lead.objects.all()
        status = self.request.query_params.get('status', None)
        lead_type = self.request.query_params.get('lead_type', None)
        assigned_agent = self.request.query_params.get('assigned_agent', None)
        
        if status:
            queryset = queryset.filter(status=status)
        if lead_type:
            queryset = queryset.filter(lead_type=lead_type)
        if assigned_agent:
            queryset = queryset.filter(assigned_agent_id=assigned_agent)
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update lead status"""
        lead = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Lead.LEAD_STATUS_CHOICES):
            lead.status = new_status
            lead.save()
            
            # Create activity record
            Activity.objects.create(
                activity_type='note',
                subject=f'Status updated to {lead.get_status_display()}',
                lead=lead,
                created_by=request.user
            )
            
            return Response({'status': 'success'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def assign_agent(self, request, pk=None):
        """Assign lead to agent"""
        lead = self.get_object()
        agent_id = request.data.get('agent_id')
        
        try:
            agent = User.objects.get(id=agent_id)
            lead.assigned_agent = agent
            lead.save()
            
            # Create activity record
            Activity.objects.create(
                activity_type='note',
                subject=f'Lead assigned to {agent.get_full_name()}',
                lead=lead,
                created_by=request.user
            )
            
            return Response({'status': 'success'})
        except User.DoesNotExist:
            return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

class LeadSourceViewSet(viewsets.ModelViewSet):
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    permission_classes = [IsAuthenticated]

# ============================================================================
# TRANSACTION MANAGEMENT VIEWSETS
# ============================================================================

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaction.objects.all()
        status = self.request.query_params.get('status', None)
        agent = self.request.query_params.get('agent', None)
        
        if status:
            queryset = queryset.filter(status=status)
        if agent:
            queryset = queryset.filter(
                Q(listing_agent_id=agent) | Q(buyer_agent_id=agent)
            )
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update transaction status"""
        transaction = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Transaction.TRANSACTION_STATUS_CHOICES):
            transaction.status = new_status
            transaction.save()
            
            # Create activity record
            Activity.objects.create(
                activity_type='note',
                subject=f'Transaction status updated to {transaction.get_status_display()}',
                transaction=transaction,
                created_by=request.user
            )
            
            return Response({'status': 'success'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================
# TASK MANAGEMENT VIEWSETS
# ============================================================================

class TaskBoardViewSet(viewsets.ModelViewSet):
    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskListViewSet(viewsets.ModelViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        assigned_to = self.request.query_params.get('assigned_to', None)
        is_completed = self.request.query_params.get('is_completed', None)
        priority = self.request.query_params.get('priority', None)
        
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset.order_by('position', '-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed"""
        task = self.get_object()
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        
        return Response({'status': 'success'})
    
    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """Move task to different list"""
        task = self.get_object()
        new_list_id = request.data.get('list_id')
        new_position = request.data.get('position', 0)
        
        try:
            new_list = TaskList.objects.get(id=new_list_id)
            task.task_list = new_list
            task.position = new_position
            task.save()
            
            return Response({'status': 'success'})
        except TaskList.DoesNotExist:
            return Response({'error': 'Task list not found'}, status=status.HTTP_404_NOT_FOUND)

# ============================================================================
# PROPERTY MANAGEMENT VIEWSETS
# ============================================================================

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    permission_classes = [AllowAny]  # Public access for property listings
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListSerializer
        return PropertySerializer
    
    def get_queryset(self):
        queryset = Property.objects.all()
        
        # Filtering parameters
        status = self.request.query_params.get('status', None)
        property_type = self.request.query_params.get('property_type', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        bedrooms = self.request.query_params.get('bedrooms', None)
        bathrooms = self.request.query_params.get('bathrooms', None)
        city = self.request.query_params.get('city', None)
        
        if status:
            queryset = queryset.filter(status=status)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if min_price:
            queryset = queryset.filter(list_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(list_price__lte=max_price)
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)
        if bathrooms:
            queryset = queryset.filter(bathrooms__gte=bathrooms)
        if city:
            queryset = queryset.filter(city__icontains=city)
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment property view count"""
        property = self.get_object()
        property.view_count += 1
        property.save()
        return Response({'views': property.view_count})
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle property favorite status"""
        property = self.get_object()
        # This would typically be user-specific, but for now just increment count
        property.favorite_count += 1
        property.save()
        return Response({'favorites': property.favorite_count})

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]

# ============================================================================
# ACTIVITY TRACKING VIEWSETS
# ============================================================================

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        lead_id = self.request.query_params.get('lead_id', None)
        transaction_id = self.request.query_params.get('transaction_id', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        if transaction_id:
            queryset = queryset.filter(transaction_id=transaction_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
            
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ============================================================================
# SITE SETTINGS VIEWSETS
# ============================================================================

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Get public site settings for frontend"""
        try:
            settings = SiteSettings.objects.first()
            if settings:
                public_data = {
                    'site_name': settings.site_name,
                    'tagline': settings.tagline,
                    'phone': settings.phone,
                    'email': settings.email,
                    'address': settings.address,
                    'facebook_url': settings.facebook_url,
                    'instagram_url': settings.instagram_url,
                    'linkedin_url': settings.linkedin_url,
                    'twitter_url': settings.twitter_url,
                    'primary_color': settings.primary_color,
                    'secondary_color': settings.secondary_color,
                    'accent_color': settings.accent_color,
                }
                return Response(public_data)
            return Response({})
        except SiteSettings.DoesNotExist:
            return Response({})

# ============================================================================
# USER MANAGEMENT VIEWSETS
# ============================================================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def agents(self, request):
        """Get list of agents (staff users)"""
        agents = User.objects.filter(is_staff=True, is_active=True)
        serializer = self.get_serializer(agents, many=True)
        return Response(serializer.data)

# ============================================================================
# PUBLIC API ENDPOINTS (For Lead Capture)
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def capture_lead(request):
    """Public endpoint for lead capture from website forms"""
    serializer = LeadCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Set default source if not provided
        if not serializer.validated_data.get('source'):
            website_source, created = LeadSource.objects.get_or_create(
                name='Website',
                defaults={'description': 'Leads from website forms'}
            )
            serializer.validated_data['source'] = website_source
        
        lead = serializer.save()
        
        # Create initial activity
        Activity.objects.create(
            activity_type='note',
            subject='New lead captured from website',
            description=f'Lead submitted through website form',
            lead=lead,
            created_by_id=1  # System user
        )
        
        return Response({
            'status': 'success',
            'message': 'Thank you for your interest! We will contact you soon.',
            'lead_id': str(lead.id)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def property_search(request):
    """Public property search endpoint"""
    queryset = Property.objects.filter(status='active')
    
    # Search parameters
    query = request.query_params.get('q', None)
    if query:
        queryset = queryset.filter(
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Apply other filters
    property_type = request.query_params.get('property_type', None)
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)
    bedrooms = request.query_params.get('bedrooms', None)
    bathrooms = request.query_params.get('bathrooms', None)
    
    if property_type:
        queryset = queryset.filter(property_type=property_type)
    if min_price:
        queryset = queryset.filter(list_price__gte=min_price)
    if max_price:
        queryset = queryset.filter(list_price__lte=max_price)
    if bedrooms:
        queryset = queryset.filter(bedrooms__gte=bedrooms)
    if bathrooms:
        queryset = queryset.filter(bathrooms__gte=bathrooms)
    
    # Pagination
    page_size = int(request.query_params.get('page_size', 12))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    total_count = queryset.count()
    properties = queryset[start:end]
    
    serializer = PropertyListSerializer(properties, many=True)
    
    return Response({
        'results': serializer.data,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size
    })

