# Comprehensive API views for Revolution CRM frontend

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json

# Sample data for the CRM (this would normally come from the database)
def get_sample_leads():
    return [
        {
            "id": 1,
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "(555) 123-4567",
            "status": "hot",
            "score": 85,
            "source": "Website",
            "budget": "$450,000 - $550,000",
            "preferences": "3-4 BR, Modern, Downtown",
            "lastContact": "2 hours ago",
            "avatar": "/api/placeholder/32/32"
        },
        {
            "id": 2,
            "name": "Michael Chen",
            "email": "m.chen@email.com",
            "phone": "(555) 234-5678",
            "status": "qualified",
            "score": 72,
            "source": "Facebook Ads",
            "budget": "$300,000 - $400,000",
            "preferences": "2-3 BR, Family-friendly",
            "lastContact": "1 day ago",
            "avatar": "/api/placeholder/32/32"
        },
        {
            "id": 3,
            "name": "Emily Rodriguez",
            "email": "emily.r@email.com",
            "phone": "(555) 345-6789",
            "status": "nurturing",
            "score": 58,
            "source": "Zillow",
            "budget": "$200,000 - $300,000",
            "preferences": "Starter home, Good schools",
            "lastContact": "3 days ago",
            "avatar": "/api/placeholder/32/32"
        }
    ]

def get_sample_properties():
    return [
        {
            "id": 1,
            "address": "123 Oak Street, Downtown",
            "price": "$485,000",
            "beds": 3,
            "baths": 2,
            "sqft": "1,850",
            "status": "Active",
            "daysOnMarket": 12,
            "views": 247,
            "leads": 8,
            "favorites": 15,
            "agent": "John Smith",
            "image": "/api/placeholder/300/200"
        },
        {
            "id": 2,
            "address": "456 Pine Avenue, Suburbs",
            "price": "$325,000",
            "beds": 2,
            "baths": 2,
            "sqft": "1,200",
            "status": "Pending",
            "daysOnMarket": 45,
            "views": 189,
            "leads": 12,
            "favorites": 23,
            "agent": "Lisa Davis",
            "image": "/api/placeholder/300/200"
        },
        {
            "id": 3,
            "address": "789 Maple Drive, Uptown",
            "price": "$675,000",
            "beds": 4,
            "baths": 3,
            "sqft": "2,400",
            "status": "Sold",
            "daysOnMarket": 8,
            "views": 312,
            "leads": 18,
            "favorites": 31,
            "agent": "Mike Johnson",
            "image": "/api/placeholder/300/200"
        }
    ]

def get_sample_transactions():
    return [
        {
            "id": 1,
            "property": "123 Oak Street",
            "client": "Sarah Johnson",
            "agent": "John Smith",
            "price": "$485,000",
            "commission": "$14,550",
            "status": "Under Contract",
            "closeDate": "2024-08-15",
            "daysToClose": 23
        },
        {
            "id": 2,
            "property": "456 Pine Avenue",
            "client": "Michael Chen",
            "agent": "Lisa Davis",
            "price": "$325,000",
            "commission": "$9,750",
            "status": "Pending",
            "closeDate": "2024-08-22",
            "daysToClose": 30
        },
        {
            "id": 3,
            "property": "789 Maple Drive",
            "client": "Emily Rodriguez",
            "agent": "Mike Johnson",
            "price": "$275,000",
            "commission": "$8,250",
            "status": "Closed",
            "closeDate": "2024-07-18",
            "daysToClose": 0
        }
    ]

def get_sample_tasks():
    return [
        {
            "id": 1,
            "title": "Follow up with Sarah Johnson",
            "description": "Schedule property viewing for downtown listings",
            "priority": "High",
            "status": "To Do",
            "dueDate": "2024-07-26",
            "assignee": "John Smith",
            "leadId": 1
        },
        {
            "id": 2,
            "title": "Prepare market analysis",
            "description": "Create CMA for Pine Avenue property",
            "priority": "Medium",
            "status": "In Progress",
            "dueDate": "2024-07-28",
            "assignee": "Lisa Davis",
            "leadId": 2
        },
        {
            "id": 3,
            "title": "Contract review",
            "description": "Review purchase agreement terms",
            "priority": "High",
            "status": "Done",
            "dueDate": "2024-07-24",
            "assignee": "Mike Johnson",
            "leadId": 3
        }
    ]

def get_dashboard_stats():
    return {
        "totalLeads": 1247,
        "leadsGrowth": 12.5,
        "activeProperties": 892,
        "propertiesGrowth": 8.2,
        "monthlyRevenue": 67000,
        "revenueGrowth": 15.3,
        "conversionRate": 24.8,
        "conversionGrowth": 2.1
    }

def get_revenue_data():
    return [
        {"month": "Jan", "revenue": 45000, "leads": 120},
        {"month": "Feb", "revenue": 52000, "leads": 135},
        {"month": "Mar", "revenue": 48000, "leads": 128},
        {"month": "Apr", "revenue": 61000, "leads": 142},
        {"month": "May", "revenue": 55000, "leads": 138},
        {"month": "Jun", "revenue": 67000, "leads": 156}
    ]

def get_lead_distribution():
    return [
        {"name": "Website", "value": 35, "color": "#3b82f6"},
        {"name": "Facebook Ads", "value": 25, "color": "#10b981"},
        {"name": "Zillow", "value": 20, "color": "#f59e0b"},
        {"name": "Referrals", "value": 15, "color": "#ef4444"},
        {"name": "Other", "value": 5, "color": "#8b5cf6"}
    ]

def get_activity_data():
    return [
        {"type": "Phone Calls", "count": 47},
        {"type": "Emails", "count": 128},
        {"type": "Meetings", "count": 23},
        {"type": "Showings", "count": 15}
    ]

def get_recent_activities():
    return [
        {
            "id": 1,
            "type": "Phone Call",
            "description": "Called Sarah Johnson about property viewing",
            "agent": "John Smith",
            "time": "2 hours ago",
            "duration": "15 min"
        },
        {
            "id": 2,
            "type": "Email",
            "description": "Sent market analysis to Michael Chen",
            "agent": "Lisa Davis",
            "time": "4 hours ago",
            "duration": None
        },
        {
            "id": 3,
            "type": "Meeting",
            "description": "Client consultation with Emily Rodriguez",
            "agent": "Mike Johnson",
            "time": "1 day ago",
            "duration": "45 min"
        }
    ]

# API Endpoints
@csrf_exempt
@require_http_methods(["GET"])
def api_leads(request):
    """Get all leads"""
    return JsonResponse({"leads": get_sample_leads()})

@csrf_exempt
@require_http_methods(["GET"])
def api_properties(request):
    """Get all properties"""
    return JsonResponse({"properties": get_sample_properties()})

@csrf_exempt
@require_http_methods(["GET"])
def api_transactions(request):
    """Get all transactions"""
    return JsonResponse({"transactions": get_sample_transactions()})

@csrf_exempt
@require_http_methods(["GET"])
def api_tasks(request):
    """Get all tasks"""
    return JsonResponse({"tasks": get_sample_tasks()})

@csrf_exempt
@require_http_methods(["GET"])
def api_dashboard_stats(request):
    """Get dashboard statistics"""
    return JsonResponse({
        "stats": get_dashboard_stats(),
        "revenueData": get_revenue_data(),
        "leadDistribution": get_lead_distribution()
    })

@csrf_exempt
@require_http_methods(["GET"])
def api_activities(request):
    """Get activity data"""
    return JsonResponse({
        "activityData": get_activity_data(),
        "recentActivities": get_recent_activities()
    })

@csrf_exempt
@require_http_methods(["POST"])
def api_create_lead(request):
    """Create a new lead"""
    try:
        data = json.loads(request.body)
        # In a real application, you would save this to the database
        new_lead = {
            "id": len(get_sample_leads()) + 1,
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "status": "new",
            "score": 50,
            "source": data.get("source", "Manual"),
            "budget": data.get("budget", ""),
            "preferences": data.get("preferences", ""),
            "lastContact": "Just now",
            "avatar": "/api/placeholder/32/32"
        }
        return JsonResponse({"success": True, "lead": new_lead})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_create_property(request):
    """Create a new property"""
    try:
        data = json.loads(request.body)
        # In a real application, you would save this to the database
        new_property = {
            "id": len(get_sample_properties()) + 1,
            "address": data.get("address", ""),
            "price": data.get("price", ""),
            "beds": data.get("beds", 0),
            "baths": data.get("baths", 0),
            "sqft": data.get("sqft", ""),
            "status": "Active",
            "daysOnMarket": 0,
            "views": 0,
            "leads": 0,
            "favorites": 0,
            "agent": data.get("agent", ""),
            "image": "/api/placeholder/300/200"
        }
        return JsonResponse({"success": True, "property": new_property})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_create_task(request):
    """Create a new task"""
    try:
        data = json.loads(request.body)
        # In a real application, you would save this to the database
        new_task = {
            "id": len(get_sample_tasks()) + 1,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "priority": data.get("priority", "Medium"),
            "status": "To Do",
            "dueDate": data.get("dueDate", ""),
            "assignee": data.get("assignee", ""),
            "leadId": data.get("leadId", None)
        }
        return JsonResponse({"success": True, "task": new_task})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def api_update_lead(request, lead_id):
    """Update a lead"""
    try:
        data = json.loads(request.body)
        # In a real application, you would update the database
        return JsonResponse({"success": True, "message": f"Lead {lead_id} updated successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_lead(request, lead_id):
    """Delete a lead"""
    try:
        # In a real application, you would delete from the database
        return JsonResponse({"success": True, "message": f"Lead {lead_id} deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

