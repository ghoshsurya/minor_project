from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPortal(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class JobListing(models.Model):
    portal = models.ForeignKey(JobPortal, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    experience_required = models.CharField(max_length=50)
    salary_range = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    job_url = models.URLField()
    posted_date = models.DateTimeField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    is_recent = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-posted_date']
        unique_together = ['portal', 'job_url']
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class UserJobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert for {self.user.username} - {self.keywords}"