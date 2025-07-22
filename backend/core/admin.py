from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *

# Customize the admin site header and title
admin.site.site_header = "Revolution Realty Administration"
admin.site.site_title = "Revolution Realty Admin"
admin.site.index_title = "Welcome to Revolution Realty Administration"

# User Management (Enhanced)
class UserProfileInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('last_login', 'date_joined')}),
    )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Role Management
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

# User Authentication & Security
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
    list_display = ('id', 'user_id', 'client_id', 'created_at', 'updated_at')
    list_filter = ('client_id', 'created_at')
    search_fields = ('user_id',)

@admin.register(DatProjects)
class DatProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'client_id', 'created_at', 'updated_at')
    list_filter = ('client_id', 'created_at')
    search_fields = ('user_id',)

@admin.register(DatProjectsImages)
class DatProjectsImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('project_id',)

@admin.register(DatProjectsVideos)
class DatProjectsVideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('project_id',)

# Property & Listing Management
@admin.register(UserBookmarkProject)
class UserBookmarkProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'project_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id', 'project_id')

# Reviews & Ratings
@admin.register(VendorRating)
class VendorRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'vendor_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id', 'vendor_id')

@admin.register(CommentReview)
class CommentReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id',)

@admin.register(DatLikeReviews)
class DatLikeReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'review_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id', 'review_id')

# Communication & Contact Management
@admin.register(MailActivityLog)
class MailActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MailSignature)
class MailSignatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id',)

@admin.register(ContactsSearches)
class ContactsSearchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user_id',)

# Route Management
@admin.register(RouteMatrix)
class RouteMatrixAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at',)

# Custom Admin Actions
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = "Mark selected items as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = "Mark selected items as inactive"

# Add custom CSS for admin styling
class AdminStyleMixin:
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

# Apply styling to all admin classes
for model_admin in [CustomUserAdmin, RoleAdmin, RoleUserAdmin, ActivationAdmin, 
                   PersistenceAdmin, ReminderAdmin, ThrottleAdmin]:
    if hasattr(model_admin, 'Media'):
        model_admin.Media.css = getattr(model_admin.Media, 'css', {})
        model_admin.Media.css['all'] = getattr(model_admin.Media.css, 'all', []) + ['admin/css/custom_admin.css']

