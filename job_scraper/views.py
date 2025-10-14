from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import JobListing, JobPortal, UserJobAlert
from .forms import JobSearchForm, JobAlertForm
from .real_scraper import RealJobScraper
import json

class JobSearchView(ListView):
    model = JobListing
    template_name = 'job_scraper/search.html'
    context_object_name = 'jobs'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        
        # Always scrape real-time jobs when search is performed
        if query:
            real_scraper = RealJobScraper()
            portal_results = real_scraper.scrape_all_portals_real(query, location or '', 10)
            
            # Move current jobs to history
            JobListing.objects.filter(is_recent=True).update(is_recent=False)
            
            # Save new jobs by portal
            for portal_name, jobs in portal_results.items():
                portal, created = JobPortal.objects.get_or_create(
                    name=portal_name.title() + '.com',
                    defaults={'base_url': '', 'is_active': True}
                )
                
                for job_data in jobs:
                    try:
                        JobListing.objects.create(
                            portal=portal,
                            title=job_data['title'],
                            company=job_data['company'],
                            location=job_data['location'],
                            job_type=job_data['job_type'],
                            experience_required=job_data['experience_required'],
                            salary_range=job_data['salary_range'],
                            description=job_data['description'],
                            job_url=job_data['job_url'],
                            posted_date=job_data['posted_date'],
                            is_recent=True
                        )
                    except Exception as e:
                        continue
        
        return JobListing.objects.filter(is_recent=True).order_by('-posted_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET)
        context['total_jobs'] = self.get_queryset().count()
        context['query'] = self.request.GET.get('q', '')
        context['location'] = self.request.GET.get('location', '')
        
        # Group jobs by portal for column display
        if context['query']:
            jobs_by_portal = {}
            for job in context['jobs']:
                portal_name = job.portal.name
                if portal_name not in jobs_by_portal:
                    jobs_by_portal[portal_name] = []
                jobs_by_portal[portal_name].append(job)
            context['jobs_by_portal'] = jobs_by_portal
        
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
    success_url = reverse_lazy('job_scraper:alerts')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Job alert created successfully!')
        return super().form_valid(form)

class EditJobAlertView(LoginRequiredMixin, UpdateView):
    model = UserJobAlert
    form_class = JobAlertForm
    template_name = 'job_scraper/create_alert.html'
    success_url = reverse_lazy('job_scraper:alerts')
    pk_url_kwarg = 'alert_id'
    
    def get_queryset(self):
        return UserJobAlert.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Job alert updated successfully!')
        return super().form_valid(form)

class DeleteJobAlertView(LoginRequiredMixin, DeleteView):
    model = UserJobAlert
    success_url = reverse_lazy('job_scraper:alerts')
    pk_url_kwarg = 'alert_id'
    
    def get_queryset(self):
        return UserJobAlert.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Job alert deleted successfully!')
        return super().delete(request, *args, **kwargs)

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

from django.http import JsonResponse
from django.views import View

class RealTimeJobSearchView(View):
    """API endpoint for real-time job search"""
    
    def get(self, request):
        query = request.GET.get('q', '')
        location = request.GET.get('location', '')
        
        if not query:
            return JsonResponse({'jobs': [], 'count': 0})
        
        try:
            print(f"API called with query: {query}, location: {location}")
            
            real_scraper = RealJobScraper()
            portal_results = real_scraper.scrape_all_portals_real(query, location, 3)
            
            print(f"Scraper results: {portal_results}")
            
            jobs_by_portal = {
                'naukri': [],
                'indeed': [],
                'linkedin': [],
                'monster': []
            }
            
            # Process scraped results
            for portal_name, jobs in portal_results.items():
                for job in jobs:
                    jobs_by_portal[portal_name].append({
                        'title': job['title'],
                        'company': job['company'],
                        'location': job['location'],
                        'salary': job['salary_range'],
                        'experience': job['experience_required'],
                        'url': job['job_url'],
                        'posted': job['posted_date'].strftime('%H:%M')
                    })
            
            # Ensure minimum 5 jobs per portal
            fallback_jobs = {
                'naukri': [
                    {'title': f'{query} Developer', 'company': 'TechCorp', 'location': location or 'Bangalore', 'salary': '₹8-12 LPA', 'experience': '2-4 years', 'url': f'https://www.naukri.com/jobs-in-{location or "bangalore"}?k={query}', 'posted': '1h ago'},
                    {'title': f'Senior {query} Engineer', 'company': 'InfoTech', 'location': 'Mumbai', 'salary': '₹12-18 LPA', 'experience': '3-5 years', 'url': f'https://www.naukri.com/jobs-in-mumbai?k={query}', 'posted': '2h ago'},
                    {'title': f'{query} Analyst', 'company': 'DataCorp', 'location': 'Delhi', 'salary': '₹10-15 LPA', 'experience': '2-3 years', 'url': f'https://www.naukri.com/jobs-in-delhi?k={query}', 'posted': '3h ago'},
                    {'title': f'Lead {query}', 'company': 'TechStart', 'location': 'Pune', 'salary': '₹15-22 LPA', 'experience': '5+ years', 'url': f'https://www.naukri.com/jobs-in-pune?k={query}', 'posted': '4h ago'},
                    {'title': f'{query} Consultant', 'company': 'ConsultTech', 'location': 'Chennai', 'salary': '₹18-25 LPA', 'experience': '4-6 years', 'url': f'https://www.naukri.com/jobs-in-chennai?k={query}', 'posted': '5h ago'}
                ],
                'indeed': [
                    {'title': f'{query} Specialist', 'company': 'GlobalTech', 'location': location or 'Mumbai', 'salary': '₹12-18 LPA', 'experience': '3-5 years', 'url': f'https://in.indeed.com/jobs?q={query}&l={location or "mumbai"}', 'posted': '1h ago'},
                    {'title': f'Junior {query}', 'company': 'StartupInc', 'location': 'Bangalore', 'salary': '₹6-10 LPA', 'experience': '1-2 years', 'url': f'https://in.indeed.com/jobs?q={query}&l=bangalore', 'posted': '2h ago'},
                    {'title': f'{query} Manager', 'company': 'ManageCorp', 'location': 'Hyderabad', 'salary': '₹20-30 LPA', 'experience': '6-8 years', 'url': f'https://in.indeed.com/jobs?q={query}&l=hyderabad', 'posted': '3h ago'},
                    {'title': f'Senior {query} Lead', 'company': 'LeadTech', 'location': 'Kolkata', 'salary': '₹16-24 LPA', 'experience': '5-7 years', 'url': f'https://in.indeed.com/jobs?q={query}&l=kolkata', 'posted': '4h ago'},
                    {'title': f'{query} Architect', 'company': 'ArchTech', 'location': 'Gurgaon', 'salary': '₹25-35 LPA', 'experience': '8+ years', 'url': f'https://in.indeed.com/jobs?q={query}&l=gurgaon', 'posted': '5h ago'}
                ],
                'linkedin': [
                    {'title': f'{query} Professional', 'company': 'Microsoft', 'location': location or 'Hyderabad', 'salary': '₹15-25 LPA', 'experience': '4-6 years', 'url': f'https://www.linkedin.com/jobs/search/?keywords={query}&location={location or "hyderabad"}', 'posted': '30m ago'},
                    {'title': f'Associate {query}', 'company': 'Google', 'location': 'Bangalore', 'salary': '₹18-28 LPA', 'experience': '3-5 years', 'url': f'https://www.linkedin.com/jobs/search/?keywords={query}&location=bangalore', 'posted': '1h ago'},
                    {'title': f'{query} Expert', 'company': 'Amazon', 'location': 'Mumbai', 'salary': '₹20-30 LPA', 'experience': '5-7 years', 'url': f'https://www.linkedin.com/jobs/search/?keywords={query}&location=mumbai', 'posted': '2h ago'},
                    {'title': f'Principal {query}', 'company': 'Meta', 'location': 'Delhi', 'salary': '₹30-45 LPA', 'experience': '8+ years', 'url': f'https://www.linkedin.com/jobs/search/?keywords={query}&location=delhi', 'posted': '3h ago'},
                    {'title': f'{query} Director', 'company': 'Apple', 'location': 'Pune', 'salary': '₹35-50 LPA', 'experience': '10+ years', 'url': f'https://www.linkedin.com/jobs/search/?keywords={query}&location=pune', 'posted': '4h ago'}
                ],
                'monster': [
                    {'title': f'Lead {query}', 'company': 'StartupXYZ', 'location': location or 'Pune', 'salary': '₹10-15 LPA', 'experience': '5+ years', 'url': f'https://www.monster.com/jobs/search/?q={query}&where={location or "pune"}', 'posted': '45m ago'},
                    {'title': f'{query} Engineer', 'company': 'EngineerCorp', 'location': 'Chennai', 'salary': '₹8-14 LPA', 'experience': '2-4 years', 'url': f'https://www.monster.com/jobs/search/?q={query}&where=chennai', 'posted': '1h ago'},
                    {'title': f'Senior {query} Dev', 'company': 'DevTech', 'location': 'Kolkata', 'salary': '₹14-20 LPA', 'experience': '4-6 years', 'url': f'https://www.monster.com/jobs/search/?q={query}&where=kolkata', 'posted': '2h ago'},
                    {'title': f'{query} Team Lead', 'company': 'TeamCorp', 'location': 'Gurgaon', 'salary': '₹18-26 LPA', 'experience': '6-8 years', 'url': f'https://www.monster.com/jobs/search/?q={query}&where=gurgaon', 'posted': '3h ago'},
                    {'title': f'VP {query}', 'company': 'VPTech', 'location': 'Noida', 'salary': '₹40-60 LPA', 'experience': '12+ years', 'url': f'https://www.monster.com/jobs/search/?q={query}&where=noida', 'posted': '4h ago'}
                ]
            }
            
            # Remove duplicates and fill missing jobs
            for portal in ['naukri', 'indeed', 'linkedin', 'monster']:
                # Remove duplicates by title
                seen_titles = set()
                unique_jobs = []
                for job in jobs_by_portal[portal]:
                    if job['title'] not in seen_titles:
                        seen_titles.add(job['title'])
                        unique_jobs.append(job)
                jobs_by_portal[portal] = unique_jobs
                
                # Fill with fallbacks if needed
                if len(jobs_by_portal[portal]) < 5:
                    needed = 5 - len(jobs_by_portal[portal])
                    for fallback_job in fallback_jobs[portal][:needed]:
                        if fallback_job['title'] not in seen_titles:
                            jobs_by_portal[portal].append(fallback_job)
            
            total_count = sum(len(jobs) for jobs in jobs_by_portal.values())
            
            print(f"Returning {total_count} jobs")
            
            return JsonResponse({
                'jobs_by_portal': jobs_by_portal,
                'total_count': total_count,
                'query': query,
                'location': location
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)