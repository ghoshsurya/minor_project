from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from accounts.models import CustomUser

class CVUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=200)
    original_cv = models.FileField(upload_to='cvs/original/')
    optimized_cv = models.FileField(upload_to='cvs/optimized/', blank=True, null=True)
    ats_score = models.FloatField(default=0.0)
    
    # Gemini AI Analysis Fields
    gemini_analysis = models.JSONField(default=dict, blank=True)
    missing_sections = models.JSONField(default=list, blank=True)
    improvement_suggestions = models.JSONField(default=list, blank=True)
    keyword_suggestions = models.JSONField(default=list, blank=True)
    job_match_percentage = models.FloatField(default=0.0)
    optimized_content = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.job_role}"
    
    def get_job_role_slug(self):
        return slugify(self.job_role)
    
    def get_unique_id(self):
        # Get user's CV count for this specific job role
        user_cvs = CVUpload.objects.filter(
            user=self.user, 
            job_role=self.job_role
        ).order_by('created_at')
        
        for index, cv in enumerate(user_cvs, 1):
            if cv.id == self.id:
                return index
        return 1

class ATSKeyword(models.Model):
    keyword = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.keyword

class CVTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('creative', 'Creative'),
        ('professional', 'Professional'),
        ('minimal', 'Minimal'),
    ]
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    description = models.TextField()
    html_template = models.TextField()
    css_styles = models.TextField()
    is_active = models.BooleanField(default=True)
    preview_image = models.ImageField(upload_to='cv_templates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.template_type})"

class CreatedCV(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    template = models.ForeignKey(CVTemplate, on_delete=models.CASCADE)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Professional Summary
    professional_summary = models.TextField(blank=True)
    
    # Experience (JSON field to store multiple experiences)
    experience = models.JSONField(default=list, blank=True)
    
    # Education (JSON field to store multiple education entries)
    education = models.JSONField(default=list, blank=True)
    
    # Skills (JSON field to store skills by category)
    skills = models.JSONField(default=dict, blank=True)
    
    # Additional sections
    certifications = models.JSONField(default=list, blank=True)
    projects = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    
    # Generated files
    pdf_file = models.FileField(upload_to='created_cvs/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.template.name}"