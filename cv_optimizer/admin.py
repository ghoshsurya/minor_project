from django.contrib import admin
from .models import CVUpload, ATSKeyword, JobDescription

@admin.register(CVUpload)
class CVUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_role', 'ats_score', 'created_at')
    list_filter = ('job_role', 'created_at', 'ats_score')
    search_fields = ('user__username', 'user__email', 'job_role')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ATSKeyword)
class ATSKeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'category', 'weight')
    list_filter = ('category',)
    search_fields = ('keyword', 'category')
    ordering = ('category', 'keyword')

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('keywords',)
    ordering = ('-created_at',)