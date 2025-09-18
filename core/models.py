from django.db import models
from django.contrib.auth.models import User

class HeroSection(models.Model):
    title = models.CharField(max_length=200, default="JobLift – AI-Powered ATS Resume Optimizer & Job Matcher")
    subtitle = models.TextField(default="Boost your career with JobLift. Optimize your CV for Applicant Tracking Systems (ATS), get a higher resume score, and discover tailored job opportunities.")
    background_video = models.URLField(blank=True, null=True, help_text="YouTube or video URL")
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    cta_text = models.CharField(max_length=50, default="Get Started")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section - {self.title[:50]}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class InterviewResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('practice', 'Practice'),
        ('tips', 'Tips'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title