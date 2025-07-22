from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as DjangoUser
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *

# Customize the admin site header and title
admin.site.site_header = "Revolution Realty Administration"
admin.site.site_title = "Revolution Realty Admin"
admin.site.index_title = "Welcome to Revolution Realty Administration"

# Enhanced Django User Admin (don't unregister, just extend)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    # Use the default fieldsets without adding duplicates
    # The default BaseUserAdmin already includes last_login and date_joined

# Re-register UserAdmin with our custom version
admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, CustomUserAdmin)

# Sentinel Authentication Models
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)

@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role_id', 'created_at', 'updated_at')
    list_filter = ('role_id', 'created_at')
    search_fields = ('user_id',)

@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code', 'completed', 'completed_at', 'created_at')
    list_filter = ('completed', 'created_at', 'completed_at')
    search_fields = ('user_id', 'code')
    readonly_fields = ('code', 'created_at', 'updated_at')

@admin.register(Persistence)
class PersistenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code', 'created_at', 'updated_at')
    search_fields = ('user_id', 'code')
    readonly_fields = ('code', 'created_at', 'updated_at')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code', 'completed', 'completed_at', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('user_id', 'code')
    readonly_fields = ('code', 'created_at', 'updated_at')

@admin.register(Throttle)
class ThrottleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type', 'ip', 'created_at', 'updated_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user_id', 'ip')

# Real Estate Content Management
@admin.register(DatAwards)
class DatAwardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id', 'title')

@admin.register(DatProjects)
class DatProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'title', 'city', 'state', 'created_at')
    list_filter = ('state', 'created_at')
    search_fields = ('user_id', 'title', 'city')

@admin.register(DatProjectsImages)
class DatProjectsImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'projects_id', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('projects_id', 'title')

@admin.register(DatProjectsVideos)
class DatProjectsVideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'projects_id', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('projects_id', 'title')

# Property & Listing Management
@admin.register(UserBookmarkProject)
class UserBookmarkProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'project_id', 'book_mark_flash', 'created_at')
    list_filter = ('book_mark_flash', 'created_at')
    search_fields = ('user_id', 'project_id')

# Reviews & Ratings
@admin.register(VendorRating)
class VendorRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user_reviewed_id', 'first_name', 'last_name', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user_id', 'first_name', 'last_name', 'email')

@admin.register(CommentReview)
class CommentReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_review', 'user_comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_comment', 'comment')

@admin.register(DatLikeReviews)
class DatLikeReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'vendor_rating_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_id', 'vendor_rating_id')

# Communication & Contact Management
@admin.register(MailActivityLog)
class MailActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_name', 'to_name', 'subject', 'send_status', 'create_at')
    list_filter = ('send_status', 'status_type', 'create_at')
    search_fields = ('from_name', 'to_name', 'subject')
    readonly_fields = ('create_at',)

@admin.register(MailSignature)
class MailSignatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'create_at', 'update_at')
    list_filter = ('status', 'create_at')
    search_fields = ('user_id',)

@admin.register(ContactsSearches)
class ContactsSearchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_id', 'type', 'region', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user_id', 'keyword')

# Route Management
@admin.register(RouteMatrix)
class RouteMatrixAdmin(admin.ModelAdmin):
    list_display = ('id', 'route_name', 'guest', 'user', 'vendor', 'agent', 'system_admin', 'super_admin')
    search_fields = ('route_name',)

# Custom Admin Actions
def make_active(modeladmin, request, queryset):
    queryset.update(status=1)
make_active.short_description = "Mark selected items as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(status=0)
make_inactive.short_description = "Mark selected items as inactive"

# Custom CSS for admin styling
class AdminStyleMixin:
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

# Apply styling to main admin classes
for model_admin in [CustomUserAdmin, RoleAdmin, RoleUserAdmin, ActivationAdmin, 
                   PersistenceAdmin, ReminderAdmin, ThrottleAdmin]:
    if hasattr(model_admin, 'Media'):
        model_admin.Media.css = getattr(model_admin.Media, 'css', {})
        model_admin.Media.css['all'] = getattr(model_admin.Media.css, 'all', []) + ['admin/css/custom_admin.css']

