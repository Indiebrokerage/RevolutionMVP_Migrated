# Revolution Realty - Comprehensive REST API Views
# Market-ready CRM API endpoints

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .serializers import *

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# ============================================================================
# LEAD MANAGEMENT API (BOOMTOWN-STYLE)
# ============================================================================

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Lead.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by temperature
        temperature = self.request.query_params.get('temperature', None)
        if temperature:
            queryset = queryset.filter(temperature=temperature)
        
        # Filter by assigned agent
        agent = self.request.query_params.get('agent', None)
        if agent:
            queryset = queryset.filter(assigned_agent_id=agent)
        
        # Filter by lead score range
        min_score = self.request.query_params.get('min_score', None)
        max_score = self.request.query_params.get('max_score', None)
        if min_score:
            queryset = queryset.filter(lead_score__gte=min_score)
        if max_score:
            queryset = queryset.filter(lead_score__lte=max_score)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update lead score based on activity"""
        lead = self.get_object()
        lead.calculate_lead_score()
        lead.save()
        return Response({'lead_score': lead.lead_score})
    
    @action(detail=True, methods=['post'])
    def add_activity(self, request, pk=None):
        """Add activity to lead"""
        lead = self.get_object()
        activity_data = request.data
        activity_data['lead'] = lead.id
        activity_data['agent'] = request.user.id
        
        serializer = ActivitySerializer(data=activity_data)
        if serializer.is_valid():
            serializer.save()
            
            # Update lead score after activity
            lead.calculate_lead_score()
            lead.last_contact = timezone.now()
            lead.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get lead dashboard statistics"""
        total_leads = Lead.objects.count()
        new_leads = Lead.objects.filter(status='new').count()
        hot_leads = Lead.objects.filter(temperature='hot').count()
        qualified_leads = Lead.objects.filter(status='qualified').count()
        
        # Leads by source
        leads_by_source = Lead.objects.values('source__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Recent leads
        recent_leads = Lead.objects.order_by('-created_at')[:10]
        recent_serializer = LeadSerializer(recent_leads, many=True)
        
        return Response({
            'total_leads': total_leads,
            'new_leads': new_leads,
            'hot_leads': hot_leads,
            'qualified_leads': qualified_leads,
            'leads_by_source': leads_by_source,
            'recent_leads': recent_serializer.data
        })

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        
        # Filter by lead
        lead_id = self.request.query_params.get('lead', None)
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent', None)
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by status
        activity_status = self.request.query_params.get('status', None)
        if activity_status:
            queryset = queryset.filter(status=activity_status)
        
        return queryset.order_by('-scheduled_at')

# ============================================================================
# TRANSACTION MANAGEMENT API (COMMISSIONS INC-STYLE)
# ============================================================================

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaction.objects.all()
        
        # Filter by status
        transaction_status = self.request.query_params.get('status', None)
        if transaction_status:
            queryset = queryset.filter(status=transaction_status)
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent', None)
        if agent_id:
            queryset = queryset.filter(
                Q(listing_agent_id=agent_id) | Q(buyer_agent_id=agent_id)
            )
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def calculate_commission(self, request, pk=None):
        """Calculate commission splits for transaction"""
        transaction = self.get_object()
        transaction.calculate_commissions()
        transaction.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pipeline_stats(self, request):
        """Get transaction pipeline statistics"""
        pipeline_data = Transaction.objects.values('status').annotate(
            count=Count('id'),
            total_volume=Sum('sale_price')
        ).order_by('status')
        
        total_volume = Transaction.objects.filter(
            status='closed'
        ).aggregate(total=Sum('sale_price'))['total'] or 0
        
        total_commission = Transaction.objects.filter(
            status='closed'
        ).aggregate(total=Sum('gross_commission'))['total'] or 0
        
        return Response({
            'pipeline': pipeline_data,
            'total_volume': total_volume,
            'total_commission': total_commission
        })

# ============================================================================
# PROPERTY MANAGEMENT API (REAL GEEKS-STYLE)
# ============================================================================

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Property.objects.all()
        
        # Filter by status
        property_status = self.request.query_params.get('status', None)
        if property_status:
            queryset = queryset.filter(status=property_status)
        
        # Filter by property type
        property_type = self.request.query_params.get('type', None)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(list_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(list_price__lte=max_price)
        
        # Filter by bedrooms/bathrooms
        bedrooms = self.request.query_params.get('bedrooms', None)
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)
        
        bathrooms = self.request.query_params.get('bathrooms', None)
        if bathrooms:
            queryset = queryset.filter(bathrooms__gte=bathrooms)
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(address__icontains=search) |
                Q(city__icontains=search) |
                Q(mls_number__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        """Track property view for analytics"""
        property_obj = self.get_object()
        property_obj.view_count += 1
        property_obj.save()
        
        # Create analytics event
        AnalyticsEvent.objects.create(
            event_type='property_view',
            property=property_obj,
            user_session=request.session.session_key or 'anonymous',
            page_url=request.META.get('HTTP_REFERER', ''),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'view_count': property_obj.view_count})
    
    @action(detail=False, methods=['get'])
    def market_stats(self, request):
        """Get property market statistics"""
        total_properties = Property.objects.count()
        active_listings = Property.objects.filter(status='active').count()
        avg_price = Property.objects.filter(
            status='active'
        ).aggregate(avg=Avg('list_price'))['avg'] or 0
        
        # Properties by type
        by_type = Property.objects.values('property_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Properties by city
        by_city = Property.objects.values('city').annotate(
            count=Count('id'),
            avg_price=Avg('list_price')
        ).order_by('-count')[:10]
        
        return Response({
            'total_properties': total_properties,
            'active_listings': active_listings,
            'average_price': avg_price,
            'by_type': by_type,
            'by_city': by_city
        })

# ============================================================================
# TASK MANAGEMENT API (ASANA/TRELLO-STYLE)
# ============================================================================

class TaskBoardViewSet(viewsets.ModelViewSet):
    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TaskBoard.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        # Filter by task list
        task_list_id = self.request.query_params.get('task_list', None)
        if task_list_id:
            queryset = queryset.filter(task_list_id=task_list_id)
        
        # Filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        # Filter by completion status
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            queryset = queryset.filter(is_completed=completed.lower() == 'true')
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('order', 'created_at')
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed"""
        task = self.get_object()
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)

# ============================================================================
# WEBSITE & CONTENT MANAGEMENT API
# ============================================================================

class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]

class WebsitePageViewSet(viewsets.ModelViewSet):
    queryset = WebsitePage.objects.all()
    serializer_class = WebsitePageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = WebsitePage.objects.all()
        
        # Filter by website
        website_id = self.request.query_params.get('website', None)
        if website_id:
            queryset = queryset.filter(website_id=website_id)
        
        return queryset.order_by('order')

class LeadCaptureFormViewSet(viewsets.ModelViewSet):
    queryset = LeadCaptureForm.objects.all()
    serializer_class = LeadCaptureFormSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Handle form submission and create lead"""
        form = self.get_object()
        form_data = request.data
        
        # Create lead from form submission
        lead_data = {
            'first_name': form_data.get('first_name', ''),
            'last_name': form_data.get('last_name', ''),
            'email': form_data.get('email', ''),
            'phone': form_data.get('phone', ''),
            'notes': form_data.get('message', ''),
            'source': form_data.get('source_id', None)
        }
        
        lead_serializer = LeadSerializer(data=lead_data)
        if lead_serializer.is_valid():
            lead = lead_serializer.save()
            
            # Update form analytics
            form.submissions += 1
            form.save()
            
            # Create analytics event
            AnalyticsEvent.objects.create(
                event_type='lead_form_submit',
                lead=lead,
                user_session=request.session.session_key or 'anonymous',
                event_data={'form_id': form.id, 'form_name': form.name}
            )
            
            return Response({
                'success': True,
                'lead_id': lead.id,
                'message': 'Thank you for your submission!'
            })
        
        return Response({
            'success': False,
            'errors': lead_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================
# ANALYTICS & REPORTING API
# ============================================================================

class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get main dashboard analytics"""
        # Date range filter
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Lead analytics
        total_leads = Lead.objects.count()
        new_leads = Lead.objects.filter(created_at__gte=start_date).count()
        
        # Transaction analytics
        total_transactions = Transaction.objects.count()
        closed_transactions = Transaction.objects.filter(status='closed').count()
        total_volume = Transaction.objects.filter(
            status='closed'
        ).aggregate(total=Sum('sale_price'))['total'] or 0
        
        # Property analytics
        total_properties = Property.objects.count()
        active_listings = Property.objects.filter(status='active').count()
        
        # Activity analytics
        recent_activities = Activity.objects.filter(
            created_at__gte=start_date
        ).count()
        
        return Response({
            'leads': {
                'total': total_leads,
                'new': new_leads,
                'conversion_rate': (closed_transactions / total_leads * 100) if total_leads > 0 else 0
            },
            'transactions': {
                'total': total_transactions,
                'closed': closed_transactions,
                'volume': total_volume
            },
            'properties': {
                'total': total_properties,
                'active': active_listings
            },
            'activities': {
                'recent': recent_activities
            }
        })
    
    @action(detail=False, methods=['get'])
    def lead_funnel(self, request):
        """Get lead funnel analytics"""
        funnel_data = Lead.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        return Response({'funnel': funnel_data})
    
    @action(detail=False, methods=['get'])
    def revenue_forecast(self, request):
        """Get revenue forecast based on pipeline"""
        pipeline_transactions = Transaction.objects.filter(
            status__in=['active', 'under_contract', 'pending']
        )
        
        forecast_data = []
        for transaction in pipeline_transactions:
            probability = {
                'active': 0.3,
                'under_contract': 0.8,
                'pending': 0.95
            }.get(transaction.status, 0)
            
            forecast_data.append({
                'transaction_id': transaction.transaction_id,
                'expected_commission': float(transaction.gross_commission * probability),
                'probability': probability,
                'closing_date': transaction.closing_date
            })
        
        return Response({'forecast': forecast_data})

# ============================================================================
# EMAIL MARKETING API
# ============================================================================

class EmailCampaignViewSet(viewsets.ModelViewSet):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def send_campaign(self, request, pk=None):
        """Send email campaign"""
        campaign = self.get_object()
        
        if campaign.is_sent:
            return Response({
                'error': 'Campaign has already been sent'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get recipients
        recipients = campaign.recipient_list.all()
        
        # TODO: Implement actual email sending logic
        # For now, just mark as sent
        campaign.is_sent = True
        campaign.sent_at = timezone.now()
        campaign.sent_count = recipients.count()
        campaign.save()
        
        return Response({
            'success': True,
            'sent_count': campaign.sent_count
        })

# ============================================================================
# NOTIFICATION API
# ============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        return Response({'success': True})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({'success': True})

