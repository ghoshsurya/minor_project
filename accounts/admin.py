from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('profile_image_tag', 'username', 'full_name', 'email', 'phone', 'preferred_job_role', 'experience_level', 'last_updated', 'is_active')
    list_filter = ('experience_level', 'is_staff', 'is_active', 'date_joined', 'updated_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'preferred_job_role', 'phone')
    ordering = ('-updated_at',)
    list_editable = ('is_active', 'preferred_job_role', 'experience_level')
    list_per_page = 25
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('profile_picture', 'phone', 'preferred_job_role', 'experience_level'),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def profile_image_tag(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #6b7280; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">👤</div>'
        )
    profile_image_tag.short_description = 'Photo'
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    full_name.short_description = 'Full Name'
    
    def last_updated(self, obj):
        if obj.updated_at:
            time_diff = timezone.now() - obj.updated_at
            if time_diff.days > 0:
                return f"{time_diff.days} days ago"
            elif time_diff.seconds > 3600:
                return f"{time_diff.seconds // 3600} hours ago"
            elif time_diff.seconds > 60:
                return f"{time_diff.seconds // 60} minutes ago"
            else:
                return "Just now"
        return "Never"
    last_updated.short_description = 'Last Updated'