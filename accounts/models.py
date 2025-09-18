from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    preferred_job_role = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=20, choices=[
        ('fresher', 'Fresher'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5+', '5+ Years')
    ], default='fresher')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']