# Revolution Realty - SaaS Platform Setup Command
# Initialize the platform with subscription plans, features, and sample data

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.saas_models import *
from core.models import *

class Command(BaseCommand):
    help = 'Set up the SaaS platform with subscription plans, features, and sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample-tenant',
            action='store_true',
            help='Create a sample tenant with demo data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up Revolution Realty SaaS Platform...'))
        
        # Create subscription plans
        self.create_subscription_plans()
        
        # Create features
        self.create_features()
        
        # Create integrations
        self.create_integrations()
        
        # Create website templates
        self.create_website_templates()
        
        # Create onboarding steps
        self.create_onboarding_steps()
        
        # Create sample tenant if requested
        if options['create_sample_tenant']:
            self.create_sample_tenant()
        
        self.stdout.write(self.style.SUCCESS('SaaS Platform setup completed successfully!'))

    def create_subscription_plans(self):
        """Create subscription plans"""
        self.stdout.write('Creating subscription plans...')
        
        plans = [
            {
                'name': 'Starter',
                'plan_type': 'starter',
                'description': 'Perfect for individual agents just getting started',
                'monthly_price': 29.99,
                'annual_price': 299.99,
                'setup_fee': 0,
                'transaction_fee_percentage': 0.005,  # 0.5%
                'max_agents': 1,
                'max_leads_per_month': 100,
                'max_properties': 25,
                'max_storage_gb': 1,
                'features': {
                    'crm': True,
                    'lead_capture': True,
                    'basic_analytics': True,
                    'email_support': True,
                    'mobile_app': False,
                    'idx_integration': False,
                    'custom_domain': False,
                    'advanced_analytics': False,
                    'api_access': False,
                    'white_label': False
                }
            },
            {
                'name': 'Professional',
                'plan_type': 'professional',
                'description': 'Ideal for growing teams and established agents',
                'monthly_price': 79.99,
                'annual_price': 799.99,
                'setup_fee': 99.99,
                'transaction_fee_percentage': 0.003,  # 0.3%
                'max_agents': 5,
                'max_leads_per_month': 500,
                'max_properties': 100,
                'max_storage_gb': 5,
                'features': {
                    'crm': True,
                    'lead_capture': True,
                    'basic_analytics': True,
                    'email_support': True,
                    'mobile_app': True,
                    'idx_integration': True,
                    'custom_domain': True,
                    'advanced_analytics': True,
                    'api_access': True,
                    'white_label': False,
                    'priority_support': True,
                    'team_collaboration': True,
                    'automated_workflows': True
                }
            },
            {
                'name': 'Enterprise',
                'plan_type': 'enterprise',
                'description': 'For large brokerages and enterprise clients',
                'monthly_price': 199.99,
                'annual_price': 1999.99,
                'setup_fee': 299.99,
                'transaction_fee_percentage': 0.001,  # 0.1%
                'max_agents': 999,
                'max_leads_per_month': 9999,
                'max_properties': 9999,
                'max_storage_gb': 100,
                'features': {
                    'crm': True,
                    'lead_capture': True,
                    'basic_analytics': True,
                    'email_support': True,
                    'mobile_app': True,
                    'idx_integration': True,
                    'custom_domain': True,
                    'advanced_analytics': True,
                    'api_access': True,
                    'white_label': True,
                    'priority_support': True,
                    'team_collaboration': True,
                    'automated_workflows': True,
                    'custom_integrations': True,
                    'dedicated_support': True,
                    'sla_guarantee': True
                }
            }
        ]
        
        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'  ✓ Created plan: {plan.name}')
            else:
                self.stdout.write(f'  - Plan already exists: {plan.name}')

    def create_features(self):
        """Create platform features"""
        self.stdout.write('Creating platform features...')
        
        features = [
            {'name': 'CRM System', 'feature_key': 'crm', 'description': 'Complete customer relationship management'},
            {'name': 'Lead Capture Forms', 'feature_key': 'lead_capture', 'description': 'Customizable lead capture forms'},
            {'name': 'Basic Analytics', 'feature_key': 'basic_analytics', 'description': 'Basic reporting and analytics'},
            {'name': 'Advanced Analytics', 'feature_key': 'advanced_analytics', 'description': 'Advanced reporting and business intelligence', 'is_premium': True},
            {'name': 'Mobile App', 'feature_key': 'mobile_app', 'description': 'Native mobile applications', 'is_premium': True},
            {'name': 'IDX Integration', 'feature_key': 'idx_integration', 'description': 'MLS/IDX feed integration', 'is_premium': True},
            {'name': 'Custom Domain', 'feature_key': 'custom_domain', 'description': 'Use your own domain name', 'is_premium': True},
            {'name': 'API Access', 'feature_key': 'api_access', 'description': 'Full REST API access', 'is_premium': True},
            {'name': 'White Label', 'feature_key': 'white_label', 'description': 'Complete white-label branding', 'is_premium': True},
            {'name': 'Team Collaboration', 'feature_key': 'team_collaboration', 'description': 'Team workspaces and collaboration tools'},
            {'name': 'Automated Workflows', 'feature_key': 'automated_workflows', 'description': 'Marketing automation and workflows', 'is_premium': True},
            {'name': 'Custom Integrations', 'feature_key': 'custom_integrations', 'description': 'Custom third-party integrations', 'is_premium': True},
        ]
        
        for feature_data in features:
            feature, created = Feature.objects.get_or_create(
                feature_key=feature_data['feature_key'],
                defaults=feature_data
            )
            if created:
                self.stdout.write(f'  ✓ Created feature: {feature.name}')

    def create_integrations(self):
        """Create available integrations"""
        self.stdout.write('Creating integrations...')
        
        integrations = [
            {'name': 'Zapier', 'provider': 'Zapier', 'integration_type': 'automation', 'description': 'Connect with 5000+ apps'},
            {'name': 'Mailchimp', 'provider': 'Mailchimp', 'integration_type': 'email', 'description': 'Email marketing automation'},
            {'name': 'Google Analytics', 'provider': 'Google', 'integration_type': 'analytics', 'description': 'Website analytics and tracking'},
            {'name': 'Facebook Ads', 'provider': 'Facebook', 'integration_type': 'advertising', 'description': 'Social media advertising', 'is_premium': True},
            {'name': 'DocuSign', 'provider': 'DocuSign', 'integration_type': 'documents', 'description': 'Electronic signatures', 'is_premium': True},
            {'name': 'Stripe', 'provider': 'Stripe', 'integration_type': 'payment', 'description': 'Payment processing'},
            {'name': 'Twilio', 'provider': 'Twilio', 'integration_type': 'communication', 'description': 'SMS and voice communication', 'is_premium': True},
            {'name': 'MLS/IDX Feed', 'provider': 'Various', 'integration_type': 'mls', 'description': 'Real estate listing feeds', 'is_premium': True},
        ]
        
        for integration_data in integrations:
            integration, created = Integration.objects.get_or_create(
                name=integration_data['name'],
                defaults=integration_data
            )
            if created:
                self.stdout.write(f'  ✓ Created integration: {integration.name}')

    def create_website_templates(self):
        """Create website templates"""
        self.stdout.write('Creating website templates...')
        
        templates = [
            {
                'name': 'Modern Minimal',
                'description': 'Clean, modern design with minimal elements',
                'template_files': {'layout': 'modern_minimal', 'colors': 'blue_white'},
                'is_premium': False
            },
            {
                'name': 'Luxury Estate',
                'description': 'Elegant design for luxury real estate',
                'template_files': {'layout': 'luxury_estate', 'colors': 'gold_black'},
                'is_premium': True
            },
            {
                'name': 'Professional Corporate',
                'description': 'Professional design for corporate brokerages',
                'template_files': {'layout': 'professional', 'colors': 'navy_gray'},
                'is_premium': False
            },
            {
                'name': 'Vibrant Modern',
                'description': 'Colorful, energetic design for modern agents',
                'template_files': {'layout': 'vibrant_modern', 'colors': 'multi_color'},
                'is_premium': True
            }
        ]
        
        for template_data in templates:
            template, created = WebsiteTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'  ✓ Created template: {template.name}')

    def create_onboarding_steps(self):
        """Create onboarding steps"""
        self.stdout.write('Creating onboarding steps...')
        
        steps = [
            {'name': 'Welcome & Account Setup', 'description': 'Complete your account information', 'order': 1, 'is_required': True},
            {'name': 'Choose Your Template', 'description': 'Select a website template that fits your brand', 'order': 2, 'is_required': True},
            {'name': 'Customize Your Branding', 'description': 'Upload your logo and customize colors', 'order': 3, 'is_required': True},
            {'name': 'Set Up Your Domain', 'description': 'Configure your custom domain name', 'order': 4, 'is_required': False},
            {'name': 'Import Your Contacts', 'description': 'Import existing leads and contacts', 'order': 5, 'is_required': False},
            {'name': 'Configure Integrations', 'description': 'Connect your favorite tools and services', 'order': 6, 'is_required': False},
            {'name': 'Add Your First Property', 'description': 'Create your first property listing', 'order': 7, 'is_required': False},
            {'name': 'Invite Team Members', 'description': 'Add agents and team members to your account', 'order': 8, 'is_required': False},
            {'name': 'Launch Your Website', 'description': 'Go live with your new real estate website', 'order': 9, 'is_required': True},
        ]
        
        for step_data in steps:
            step, created = OnboardingStep.objects.get_or_create(
                name=step_data['name'],
                defaults=step_data
            )
            if created:
                self.stdout.write(f'  ✓ Created onboarding step: {step.name}')

    def create_sample_tenant(self):
        """Create a sample tenant with demo data"""
        self.stdout.write('Creating sample tenant...')
        
        # Create sample user
        user, created = User.objects.get_or_create(
            username='demo_agent',
            defaults={
                'email': 'demo@revolutionrealty.com',
                'first_name': 'Demo',
                'last_name': 'Agent',
                'is_staff': False,
                'is_active': True
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
        
        # Get starter plan
        starter_plan = SubscriptionPlan.objects.get(plan_type='starter')
        
        # Create sample tenant
        tenant, created = Tenant.objects.get_or_create(
            slug='demo-realty',
            defaults={
                'name': 'Demo Realty Group',
                'subdomain': 'demo',
                'domain': 'demo-realty.com',
                'owner': user,
                'contact_email': 'demo@revolutionrealty.com',
                'contact_phone': '(555) 123-4567',
                'subscription_plan': starter_plan,
                'status': 'trial',
                'trial_ends_at': timezone.now() + timedelta(days=14),
                'current_agents': 1,
                'current_leads_this_month': 0,
                'current_properties': 0,
                'storage_used_gb': 0
            }
        )
        
        if created:
            self.stdout.write(f'  ✓ Created sample tenant: {tenant.name}')
            
            # Create tenant user relationship
            TenantUser.objects.get_or_create(
                tenant=tenant,
                user=user,
                defaults={'role': 'owner'}
            )
            
            # Create branding
            branding, created = TenantBranding.objects.get_or_create(
                tenant=tenant,
                defaults={
                    'site_title': 'Demo Realty Group',
                    'tagline': 'Your Dream Home Awaits',
                    'hero_title': 'Find Your Perfect Home',
                    'hero_subtitle': 'We help you discover the home of your dreams with personalized service and expert guidance.',
                    'phone': '(555) 123-4567',
                    'email': 'info@demo-realty.com',
                    'address': '123 Main Street, Anytown, ST 12345',
                    'primary_color': '#3B82F6',
                    'secondary_color': '#10B981',
                    'accent_color': '#F59E0B'
                }
            )
            
            # Assign template
            template = WebsiteTemplate.objects.first()
            if template:
                TenantTemplate.objects.get_or_create(
                    tenant=tenant,
                    defaults={'template': template}
                )
            
            # Create sample lead sources
            lead_sources = [
                {'name': 'Website', 'description': 'Leads from website forms', 'cost_per_lead': 15.00},
                {'name': 'Facebook Ads', 'description': 'Facebook advertising campaigns', 'cost_per_lead': 25.00},
                {'name': 'Google Ads', 'description': 'Google advertising campaigns', 'cost_per_lead': 30.00},
                {'name': 'Referrals', 'description': 'Client referrals', 'cost_per_lead': 0.00},
            ]
            
            for source_data in sources:
                LeadSource.objects.get_or_create(
                    name=source_data['name'],
                    defaults=source_data
                )
            
            # Create sample leads
            website_source = LeadSource.objects.get(name='Website')
            
            sample_leads = [
                {
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'john.smith@email.com',
                    'phone': '(555) 234-5678',
                    'status': 'new',
                    'lead_type': 'buyer',
                    'source': website_source,
                    'assigned_agent': user,
                    'min_price': 250000,
                    'max_price': 400000,
                    'bedrooms': 3,
                    'bathrooms': 2,
                    'preferred_areas': 'Downtown, Midtown'
                },
                {
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'email': 'sarah.johnson@email.com',
                    'phone': '(555) 345-6789',
                    'status': 'qualified',
                    'lead_type': 'seller',
                    'source': website_source,
                    'assigned_agent': user,
                    'preferred_areas': 'Suburbs'
                }
            ]
            
            for lead_data in sample_leads:
                Lead.objects.get_or_create(
                    email=lead_data['email'],
                    defaults=lead_data
                )
            
            self.stdout.write('  ✓ Created sample data for tenant')
        else:
            self.stdout.write('  - Sample tenant already exists')
        
        self.stdout.write(self.style.SUCCESS(f'Sample tenant created: {tenant.name}'))
        self.stdout.write(f'  - Subdomain: {tenant.subdomain}.revolutionrealty.com')
        self.stdout.write(f'  - Login: demo_agent / demo123')

