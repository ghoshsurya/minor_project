import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone
from .models import JobListing, JobPortal
import time
import random

def scrape_naukri_jobs(keywords="software developer", location="", max_pages=2):
    """Scrape jobs from Naukri.com"""
    jobs = []
    
    for page in range(1, max_pages + 1):
        try:
            url = f"https://www.naukri.com/{keywords.replace(' ', '-')}-jobs"
            if location:
                url += f"-in-{location.replace(' ', '-')}"
            url += f"?k={keywords}&l={location}&p={page}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='jobTuple')
            
            for card in job_cards[:10]:  # Limit to 10 jobs per page
                try:
                    title_elem = card.find('a', class_='title')
                    company_elem = card.find('a', class_='subTitle')
                    location_elem = card.find('span', class_='locationsContainer')
                    
                    if title_elem and company_elem:
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                            'job_type': 'full-time',
                            'experience_required': 'Not specified',
                            'salary_range': 'Not disclosed',
                            'description': f"Job opportunity for {title_elem.get_text(strip=True)} at {company_elem.get_text(strip=True)}",
                            'job_url': f"https://www.naukri.com{title_elem.get('href', '')}",
                            'posted_date': timezone.now() - timedelta(hours=random.randint(1, 24))
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
            
            # Add delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"Error scraping Naukri page {page}: {str(e)}")
            continue
    
    return jobs

def scrape_indeed_jobs(keywords="software developer", location="", max_pages=2):
    """Scrape jobs from Indeed.com"""
    jobs = []
    
    for page in range(0, max_pages * 10, 10):  # Indeed uses start parameter
        try:
            url = f"https://in.indeed.com/jobs?q={keywords}&l={location}&start={page}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:10]:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    
                    if title_elem and company_elem:
                        title_link = title_elem.find('a')
                        job = {
                            'title': title_link.get_text(strip=True) if title_link else title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True),
                            'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                            'job_type': 'full-time',
                            'experience_required': 'Not specified',
                            'salary_range': 'Not disclosed',
                            'description': f"Job opportunity for {title_elem.get_text(strip=True)} at {company_elem.get_text(strip=True)}",
                            'job_url': f"https://in.indeed.com{title_link.get('href', '')}" if title_link else '',
                            'posted_date': timezone.now() - timedelta(hours=random.randint(1, 24))
                        }
                        jobs.append(job)
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"Error scraping Indeed page {page}: {str(e)}")
            continue
    
    return jobs

def create_sample_jobs():
    """Create sample job listings for demonstration"""
    sample_jobs = [
        {
            'title': 'Python Developer',
            'company': 'TechCorp Solutions',
            'location': 'Bangalore, Karnataka',
            'job_type': 'full-time',
            'experience_required': '2-4 years',
            'salary_range': '₹8-12 LPA',
            'description': 'We are looking for a skilled Python Developer to join our team. Experience with Django, Flask, and REST APIs required.',
            'job_url': 'https://example.com/job1',
            'posted_date': timezone.now() - timedelta(hours=2)
        },
        {
            'title': 'Frontend Developer',
            'company': 'WebTech Innovations',
            'location': 'Mumbai, Maharashtra',
            'job_type': 'full-time',
            'experience_required': '1-3 years',
            'salary_range': '₹6-10 LPA',
            'description': 'Join our frontend team! Experience with React, JavaScript, and modern CSS frameworks required.',
            'job_url': 'https://example.com/job2',
            'posted_date': timezone.now() - timedelta(hours=5)
        },
        {
            'title': 'Data Scientist',
            'company': 'Analytics Pro',
            'location': 'Hyderabad, Telangana',
            'job_type': 'full-time',
            'experience_required': '3-5 years',
            'salary_range': '₹12-18 LPA',
            'description': 'Seeking a Data Scientist with expertise in Python, Machine Learning, and statistical analysis.',
            'job_url': 'https://example.com/job3',
            'posted_date': timezone.now() - timedelta(hours=8)
        },
        {
            'title': 'DevOps Engineer',
            'company': 'CloudTech Systems',
            'location': 'Pune, Maharashtra',
            'job_type': 'full-time',
            'experience_required': '2-5 years',
            'salary_range': '₹10-15 LPA',
            'description': 'Looking for DevOps Engineer with AWS, Docker, Kubernetes experience.',
            'job_url': 'https://example.com/job4',
            'posted_date': timezone.now() - timedelta(hours=12)
        },
        {
            'title': 'UI/UX Designer',
            'company': 'Design Studio',
            'location': 'Delhi, NCR',
            'job_type': 'full-time',
            'experience_required': '1-3 years',
            'salary_range': '₹5-8 LPA',
            'description': 'Creative UI/UX Designer needed. Proficiency in Figma, Adobe XD, and user research required.',
            'job_url': 'https://example.com/job5',
            'posted_date': timezone.now() - timedelta(hours=15)
        }
    ]
    
    return sample_jobs

def scrape_jobs_from_portals():
    """Main function to scrape jobs from all portals"""
    total_scraped = 0
    
    # Get or create job portals
    naukri_portal, _ = JobPortal.objects.get_or_create(
        name='Naukri.com',
        defaults={'base_url': 'https://www.naukri.com', 'is_active': True}
    )
    
    indeed_portal, _ = JobPortal.objects.get_or_create(
        name='Indeed.com',
        defaults={'base_url': 'https://in.indeed.com', 'is_active': True}
    )
    
    # For demonstration, we'll create sample jobs instead of actual scraping
    # In production, you would uncomment the actual scraping functions
    
    sample_jobs = create_sample_jobs()
    
    for job_data in sample_jobs:
        try:
            job, created = JobListing.objects.get_or_create(
                portal=naukri_portal,
                job_url=job_data['job_url'],
                defaults={
                    'title': job_data['title'],
                    'company': job_data['company'],
                    'location': job_data['location'],
                    'job_type': job_data['job_type'],
                    'experience_required': job_data['experience_required'],
                    'salary_range': job_data['salary_range'],
                    'description': job_data['description'],
                    'posted_date': job_data['posted_date'],
                    'is_recent': True
                }
            )
            
            if created:
                total_scraped += 1
                
        except Exception as e:
            print(f"Error saving job: {str(e)}")
            continue
    
    # Mark old jobs as not recent
    cutoff_date = timezone.now() - timedelta(hours=24)
    JobListing.objects.filter(posted_date__lt=cutoff_date).update(is_recent=False)
    
    return total_scraped

def get_job_recommendations(user):
    """Get job recommendations based on user profile"""
    if not user.is_authenticated:
        return JobListing.objects.filter(is_recent=True)[:10]
    
    # Get jobs based on user's preferred job role
    preferred_role = getattr(user, 'preferred_job_role', '')
    
    if preferred_role:
        return JobListing.objects.filter(
            title__icontains=preferred_role,
            is_recent=True
        )[:10]
    
    return JobListing.objects.filter(is_recent=True)[:10]