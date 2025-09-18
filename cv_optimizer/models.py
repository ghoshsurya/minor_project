from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CVUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_cv = models.FileField(upload_to='cvs/original/')
    optimized_cv = models.FileField(upload_to='cvs/optimized/', blank=True, null=True)
    job_role = models.CharField(max_length=100)
    ats_score = models.FloatField(default=0.0)
    analysis_report = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class ATSKeyword(models.Model):
    keyword = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    weight = models.FloatField(default=1.0)
    
    def __str__(self):
        return self.keyword

class JobDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.ManyToManyField(ATSKeyword)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title