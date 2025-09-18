from django.contrib import admin
from .models import HeroSection, ContactMessage, InterviewResource

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'cta_text')
        }),
        ('Media', {
            'fields': ('background_video', 'background_image')
        }),
        ('Settings', {
            'fields': ('is_active',)
        })
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']

@admin.register(InterviewResource)
class InterviewResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'is_featured']
    list_filter = ['resource_type', 'category', 'is_featured']
    search_fields = ['title', 'description']