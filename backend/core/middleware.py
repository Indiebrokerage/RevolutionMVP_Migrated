# Revolution Realty - Multi-Tenant Middleware
# Handle tenant resolution and context for SaaS platform

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from .saas_models import Tenant
import threading

# Thread-local storage for tenant context
_thread_locals = threading.local()

class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to resolve tenant based on domain/subdomain
    and set tenant context for the request
    """
    
    def process_request(self, request):
        # Get the host from the request
        host = request.get_host().lower()
        
        # Remove port if present
        if ':' in host:
            host = host.split(':')[0]
        
        # Try to get tenant from cache first
        cache_key = f"tenant:{host}"
        tenant = cache.get(cache_key)
        
        if not tenant:
            tenant = self.resolve_tenant(host)
            if tenant:
                # Cache for 5 minutes
                cache.set(cache_key, tenant, 300)
        
        if not tenant:
            # If no tenant found and not accessing admin or API docs
            if not (host.startswith('admin.') or '/admin/' in request.path or '/api/docs/' in request.path):
                raise Http404("Tenant not found")
        
        # Set tenant in thread-local storage
        set_current_tenant(tenant)
        
        # Add tenant to request object
        request.tenant = tenant
        
        return None
    
    def resolve_tenant(self, host):
        """
        Resolve tenant based on host
        Priority:
        1. Custom domain (e.g., johnsmithrealty.com)
        2. Subdomain (e.g., johnsmith.revolutionrealty.com)
        """
        try:
            # First try custom domain
            tenant = Tenant.objects.get(domain=host, status='active')
            return tenant
        except Tenant.DoesNotExist:
            pass
        
        # Try subdomain
        if '.revolutionrealty.com' in host:
            subdomain = host.replace('.revolutionrealty.com', '')
            try:
                tenant = Tenant.objects.get(subdomain=subdomain, status='active')
                return tenant
            except Tenant.DoesNotExist:
                pass
        
        # For development/localhost
        if host in ['localhost', '127.0.0.1', 'revolutionmvpmigrated-production.up.railway.app']:
            # Return first active tenant for development
            return Tenant.objects.filter(status='active').first()
        
        return None
    
    def process_response(self, request, response):
        # Clear tenant context
        clear_current_tenant()
        return response

def get_current_tenant():
    """Get the current tenant from thread-local storage"""
    return getattr(_thread_locals, 'tenant', None)

def set_current_tenant(tenant):
    """Set the current tenant in thread-local storage"""
    _thread_locals.tenant = tenant

def clear_current_tenant():
    """Clear the current tenant from thread-local storage"""
    if hasattr(_thread_locals, 'tenant'):
        delattr(_thread_locals, 'tenant')

class TenantQuerySetMixin:
    """Mixin to automatically filter querysets by current tenant"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = get_current_tenant()
        
        if tenant and hasattr(self.model, 'tenant'):
            queryset = queryset.filter(tenant=tenant)
        
        return queryset

class SubscriptionMiddleware(MiddlewareMixin):
    """
    Middleware to check subscription status and limits
    """
    
    def process_request(self, request):
        tenant = getattr(request, 'tenant', None)
        
        if not tenant:
            return None
        
        # Skip checks for admin and API documentation
        if '/admin/' in request.path or '/api/docs/' in request.path:
            return None
        
        # Check if trial has expired
        if tenant.status == 'trial' and tenant.is_trial_expired():
            # Redirect to upgrade page or show trial expired message
            # For now, we'll allow access but could restrict later
            pass
        
        # Check if subscription is suspended
        if tenant.status == 'suspended':
            # Could redirect to billing page or show suspended message
            pass
        
        return None

class UsageTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track usage metrics for billing
    """
    
    def process_request(self, request):
        tenant = getattr(request, 'tenant', None)
        
        if not tenant:
            return None
        
        # Track API calls
        if request.path.startswith('/api/'):
            self.increment_usage(tenant, 'api_calls', 1)
        
        return None
    
    def increment_usage(self, tenant, metric_type, value):
        """Increment usage metric for tenant"""
        from django.utils import timezone
        from .saas_models import UsageMetric
        from datetime import datetime
        
        # Get current month period
        now = timezone.now()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get or create usage metric for current month
        metric, created = UsageMetric.objects.get_or_create(
            tenant=tenant,
            metric_type=metric_type,
            period_start=period_start,
            defaults={
                'period_end': period_start.replace(month=period_start.month + 1) if period_start.month < 12 else period_start.replace(year=period_start.year + 1, month=1),
                'value': 0
            }
        )
        
        # Increment the value
        metric.value += value
        metric.save()

class BrandingMiddleware(MiddlewareMixin):
    """
    Middleware to inject tenant branding into context
    """
    
    def process_request(self, request):
        tenant = getattr(request, 'tenant', None)
        
        if tenant:
            # Get branding configuration
            try:
                branding = tenant.branding
                request.branding = branding
            except:
                # Create default branding if doesn't exist
                from .saas_models import TenantBranding
                branding = TenantBranding.objects.create(tenant=tenant)
                request.branding = branding
        
        return None

