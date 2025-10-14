from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from .models import InterviewResource, ContactMessage, HeroSection
from cv_optimizer.models import CVUpload
from job_scraper.models import JobListing

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_section'] = HeroSection.objects.filter(is_active=True).first()
        context['featured_resources'] = InterviewResource.objects.filter(is_featured=True)[:3]
        context['recent_jobs'] = JobListing.objects.filter(is_recent=True)[:6]
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['recent_cvs'] = CVUpload.objects.filter(user=user)[:5]
        context['total_cvs'] = CVUpload.objects.filter(user=user).count()
        context['avg_score'] = CVUpload.objects.filter(user=user).aggregate(
            avg_score=models.Avg('ats_score')
        )['avg_score'] or 0
        return context

class InterviewResourcesView(TemplateView):
    template_name = 'core/resources.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = InterviewResource.objects.all()
        context['categories'] = InterviewResource.objects.values_list('category', flat=True).distinct()
        return context

class ContactView(CreateView):
    model = ContactMessage
    template_name = 'core/contact.html'
    fields = ['name', 'email', 'subject', 'message']
    
    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent successfully!')
        return redirect('core:contact')

class AboutView(TemplateView):
    template_name = 'core/about.html'

class FlowchartView(TemplateView):
    template_name = 'core/flowchart.html'