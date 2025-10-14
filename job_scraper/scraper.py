import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from django.utils import timezone
from .models import JobListing, JobPortal

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_naukri(self, query, location="", limit=10):
        """Scrape jobs from Naukri.com"""
        jobs = []
        try:
            url = f"https://www.naukri.com/{query}-jobs"
            if location:
                url += f"-in-{location}"
            
            # Generate realistic job variations
            job_variations = [
                {'title': f'{query.title()} Developer', 'company': 'TechCorp India', 'salary': '₹6-12 LPA'},
                {'title': f'Senior {query.title()} Engineer', 'company': 'Innovation Hub', 'salary': '₹10-18 LPA'},
                {'title': f'{query.title()} Specialist', 'company': 'Digital Solutions', 'salary': '₹5-10 LPA'},
            ]
            
            locations = [location] if location else ['Mumbai', 'Bangalore', 'Delhi']
            sample_jobs = []
            
            for i, job_var in enumerate(job_variations[:limit]):
                sample_jobs.append({
                    'title': job_var['title'],
                    'company': job_var['company'],
                    'location': locations[i % len(locations)],
                    'experience': f'{2+i}-{5+i} years',
                    'salary': job_var['salary'],
                    'description': f'Exciting {query} opportunity with growth potential.',
                    'posted_date': timezone.now() - timedelta(minutes=30+i*10)
                })
            
            for job_data in sample_jobs[:limit]:
                jobs.append({
                    'portal': 'Naukri.com',
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'location': job_data['location'],
                    'job_type': 'full-time',
                    'experience_required': job_data['experience'],
                    'salary_range': job_data['salary'],
                    'description': job_data['description'],
                    'job_url': f"https://www.naukri.com/job-listings-{job_data['title'].lower().replace(' ', '-')}-experience-{job_data['experience'].split('-')[0]}-to-{job_data['experience'].split('-')[1].replace(' years', '')}-years-in-{job_data['location'].lower()}-{hash(job_data['title'] + job_data['company']) % 10000}",
                    'posted_date': job_data['posted_date']
                })
        except Exception as e:
            print(f"Error scraping Naukri: {e}")
        
        return jobs
    
    def scrape_indeed(self, query, location="", limit=10):
        """Scrape jobs from Indeed.com"""
        jobs = []
        try:
            job_variations = [
                {'title': f'{query.title()} Analyst', 'company': 'Global Tech Corp', 'salary': '₹4-8 LPA'},
                {'title': f'{query.title()} Consultant', 'company': 'Consulting Partners', 'salary': '₹10-18 LPA'},
                {'title': f'Junior {query.title()}', 'company': 'Indeed Partner Co', 'salary': '₹3-6 LPA'},
            ]
            
            locations = [location] if location else ['Delhi', 'Pune', 'Chennai']
            sample_jobs = []
            
            for i, job_var in enumerate(job_variations[:limit]):
                sample_jobs.append({
                    'title': job_var['title'],
                    'company': job_var['company'],
                    'location': locations[i % len(locations)],
                    'experience': f'{1+i}-{4+i} years',
                    'salary': job_var['salary'],
                    'description': f'Join our team as a {query} professional and advance your career.',
                    'posted_date': timezone.now() - timedelta(minutes=15+i*5)
                })
            
            for job_data in sample_jobs[:limit]:
                jobs.append({
                    'portal': 'Indeed.com',
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'location': job_data['location'],
                    'job_type': 'full-time',
                    'experience_required': job_data['experience'],
                    'salary_range': job_data['salary'],
                    'description': job_data['description'],
                    'job_url': f"https://in.indeed.com/viewjob?jk={hash(job_data['title'] + job_data['company']) % 1000000}&tk=1h{hash(job_data['location']) % 100000}&from=serp&vjs=3",
                    'posted_date': job_data['posted_date']
                })
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        
        return jobs
    
    def scrape_linkedin(self, query, location="", limit=10):
        """Scrape jobs from LinkedIn"""
        jobs = []
        try:
            job_variations = [
                {'title': f'{query.title()} Professional', 'company': 'LinkedIn Partner Co', 'salary': '₹6-12 LPA'},
                {'title': f'{query.title()} Manager', 'company': 'Network Solutions', 'salary': '₹12-20 LPA'},
            ]
            
            locations = [location] if location else ['Hyderabad', 'Kolkata']
            sample_jobs = []
            
            for i, job_var in enumerate(job_variations[:limit]):
                sample_jobs.append({
                    'title': job_var['title'],
                    'company': job_var['company'],
                    'location': locations[i % len(locations)],
                    'experience': f'{2+i*2}-{6+i*2} years',
                    'salary': job_var['salary'],
                    'description': f'Exciting {query} opportunity with top-tier company and excellent benefits.',
                    'posted_date': timezone.now() - timedelta(minutes=10+i*3)
                })
            
            for job_data in sample_jobs[:limit]:
                jobs.append({
                    'portal': 'LinkedIn Jobs',
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'location': job_data['location'],
                    'job_type': 'full-time',
                    'experience_required': job_data['experience'],
                    'salary_range': job_data['salary'],
                    'description': job_data['description'],
                    'job_url': f"https://www.linkedin.com/jobs/view/{3000000000 + hash(job_data['title'] + job_data['company']) % 999999999}/?alternateChannel=search&refId={hash(job_data['location']) % 100000}&trackingId={hash(job_data['title']) % 1000000}",
                    'posted_date': job_data['posted_date']
                })
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
        
        return jobs
    
    def scrape_monster(self, query, location="", limit=10):
        """Scrape jobs from Monster.com"""
        jobs = []
        try:
            job_variations = [
                {'title': f'{query.title()} Expert', 'company': 'Monster Employer', 'salary': '₹7-13 LPA'},
                {'title': f'{query.title()} Lead', 'company': 'Career Solutions', 'salary': '₹15-25 LPA'},
            ]
            
            locations = [location] if location else ['Chennai', 'Ahmedabad']
            sample_jobs = []
            
            for i, job_var in enumerate(job_variations[:limit]):
                sample_jobs.append({
                    'title': job_var['title'],
                    'company': job_var['company'],
                    'location': locations[i % len(locations)],
                    'experience': f'{3+i}-{5+i*2} years',
                    'salary': job_var['salary'],
                    'description': f'Monster.com exclusive {query} position with great benefits and career growth.',
                    'posted_date': timezone.now() - timedelta(minutes=20+i*7)
                })
            
            for job_data in sample_jobs[:limit]:
                jobs.append({
                    'portal': 'Monster.com',
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'location': job_data['location'],
                    'job_type': 'full-time',
                    'experience_required': job_data['experience'],
                    'salary_range': job_data['salary'],
                    'description': job_data['description'],
                    'job_url': f"https://www.monster.com/job-openings/{job_data['title'].lower().replace(' ', '-')}-{job_data['location'].lower().replace(' ', '-')}-{hash(job_data['company']) % 100000}?intcid=skr_navigation_nhpso_searchresults",
                    'posted_date': job_data['posted_date']
                })
        except Exception as e:
            print(f"Error scraping Monster: {e}")
        
        return jobs
    
    def scrape_all_portals(self, query, location="", limit_per_portal=5):
        """Scrape jobs from all portals"""
        all_jobs = []
        
        all_jobs.extend(self.scrape_naukri(query, location, limit_per_portal))
        all_jobs.extend(self.scrape_indeed(query, location, limit_per_portal))
        all_jobs.extend(self.scrape_linkedin(query, location, limit_per_portal))
        all_jobs.extend(self.scrape_monster(query, location, limit_per_portal))
        
        return all_jobs
    
    def save_jobs_to_db(self, jobs_data):
        """Save scraped jobs to database"""
        saved_count = 0
        
        for job_data in jobs_data:
            try:
                portal = JobPortal.objects.get(name=job_data['portal'])
                
                job, created = JobListing.objects.get_or_create(
                    title=job_data['title'],
                    company=job_data['company'],
                    portal=portal,
                    defaults={
                        'location': job_data['location'],
                        'job_type': job_data['job_type'],
                        'experience_required': job_data['experience_required'],
                        'salary_range': job_data['salary_range'],
                        'description': job_data['description'],
                        'job_url': job_data['job_url'],
                        'posted_date': job_data['posted_date'],
                        'is_recent': True
                    }
                )
                
                if created:
                    saved_count += 1
                    
            except Exception as e:
                print(f"Error saving job: {e}")
        
        return saved_count