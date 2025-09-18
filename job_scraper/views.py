from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import JobListing, JobPortal, UserJobAlert
from .forms import JobSearchForm, JobAlertForm
from .utils import scrape_jobs_from_portals
import json

class JobSearchView(ListView):
    model = JobListing
    template_name = 'job_scraper/search.html'
    context_object_name = 'jobs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = JobListing.objects.filter(is_recent=True)
        
        # Search filters
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        job_type = self.request.GET.get('job_type')
        experience = self.request.GET.get('experience')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(company__icontains=query)
            )
        
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        if job_type:
            queryset = queryset.filter(job_type__icontains=job_type)
        
        if experience:
            queryset = queryset.filter(experience_required__icontains=experience)
        
        return queryset.order_by('-posted_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET)
        context['total_jobs'] = self.get_queryset().count()
        context['job_portals'] = JobPortal.objects.filter(is_active=True)
        return context

class JobDetailView(DetailView):
    model = JobListing
    template_name = 'job_scraper/detail.html'
    context_object_name = 'job'
    pk_url_kwarg = 'job_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        
        # Get similar jobs
        context['similar_jobs'] = JobListing.objects.filter(
            Q(title__icontains=job.title.split()[0]) |
            Q(company=job.company)
        ).exclude(id=job.id)[:5]
        
        return context

class JobAlertsView(LoginRequiredMixin, ListView):
    model = UserJobAlert
    template_name = 'job_scraper/alerts.html'
    context_object_name = 'alerts'
    
    def get_queryset(self):
        return UserJobAlert.objects.filter(user=self.request.user)

class CreateJobAlertView(LoginRequiredMixin, CreateView):
    model = UserJobAlert
    form_class = JobAlertForm
    template_name = 'job_scraper/create_alert.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Job alert created successfully!')
        return super().form_valid(form)

class ScrapeJobsView(LoginRequiredMixin, ListView):
    """Admin view to trigger job scraping"""
    model = JobListing
    template_name = 'job_scraper/scrape.html'
    
    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                # Trigger job scraping
                scraped_count = scrape_jobs_from_portals()
                messages.success(request, f'Successfully scraped {scraped_count} new jobs!')
            except Exception as e:
                messages.error(request, f'Error scraping jobs: {str(e)}')
        else:
            messages.error(request, 'Permission denied.')
        
        return self.get(request, *args, **kwargs)