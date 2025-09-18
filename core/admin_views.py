from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from cv_optimizer.models import CVUpload
from job_scraper.models import JobListing
from core.models import ContactMessage
from django.http import JsonResponse

@staff_member_required
def admin_dashboard(request):
    # Real-time statistics
    total_users = CustomUser.objects.count()
    total_cvs = CVUpload.objects.count()
    total_jobs = JobListing.objects.count()
    avg_score = CVUpload.objects.aggregate(avg_score=Avg('ats_score'))['avg_score'] or 0
    
    # Recent activity (last 24 hours)
    yesterday = timezone.now() - timedelta(days=1)
    recent_users = CustomUser.objects.filter(date_joined__gte=yesterday).count()
    recent_cvs = CVUpload.objects.filter(created_at__gte=yesterday).count()
    recent_jobs = JobListing.objects.filter(posted_date__gte=yesterday).count()
    
    # Latest activities
    try:
        latest_users = CustomUser.objects.order_by('-date_joined')[:3]
        latest_cvs = CVUpload.objects.select_related('user').order_by('-created_at')[:3]
        latest_messages = ContactMessage.objects.order_by('-created_at')[:3]
    except:
        latest_users = []
        latest_cvs = []
        latest_messages = []
    
    context = {
        'total_users': total_users,
        'total_cvs': total_cvs,
        'total_jobs': total_jobs,
        'avg_score': round(avg_score, 1),
        'recent_users': recent_users,
        'recent_cvs': recent_cvs,
        'recent_jobs': recent_jobs,
        'latest_users': latest_users,
        'latest_cvs': latest_cvs,
        'latest_messages': latest_messages,
    }
    
    return render(request, 'admin/index.html', context)