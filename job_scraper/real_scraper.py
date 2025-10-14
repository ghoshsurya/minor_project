import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, quote_plus
import random

class RealJobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_naukri(self, query, location, max_jobs=5):
        jobs = []
        try:
            search_url = f"https://www.naukri.com/{quote_plus(query)}-jobs"
            if location:
                search_url += f"-in-{quote_plus(location)}"
            
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('article', class_='jobTuple')[:max_jobs]
            
            for card in job_cards:
                try:
                    title_elem = card.find('a', class_='title')
                    title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                    job_url = urljoin('https://www.naukri.com', title_elem['href']) if title_elem else ''
                    
                    company_elem = card.find('a', class_='subTitle')
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    
                    location_elem = card.find('li', class_='fleft')
                    location_text = location_elem.get_text(strip=True) if location_elem else 'N/A'
                    
                    exp_elem = card.find('li', class_='fleft br2')
                    experience = exp_elem.get_text(strip=True) if exp_elem else 'N/A'
                    
                    salary_elem = card.find('li', class_='fleft br2')
                    salary = salary_elem.get_text(strip=True) if salary_elem else 'Not disclosed'
                    
                    posted_elem = card.find('span', class_='fleft postedDate')
                    posted_text = posted_elem.get_text(strip=True) if posted_elem else 'Recently'
                    posted_date = self.parse_posted_date(posted_text)
                    
                    desc_elem = card.find('div', class_='job-description')
                    description = desc_elem.get_text(strip=True) if desc_elem else 'No description available'
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'job_type': 'Full-time',
                        'experience_required': experience,
                        'salary_range': salary,
                        'description': description[:500],
                        'job_url': job_url,
                        'posted_date': posted_date,
                        'portal': 'Naukri.com'
                    })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping Naukri: {e}")
        
        return jobs

    def scrape_indeed(self, query, location, max_jobs=5):
        jobs = []
        try:
            search_url = f"https://in.indeed.com/jobs?q={quote_plus(query)}"
            if location:
                search_url += f"&l={quote_plus(location)}"
            
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')[:max_jobs]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    if title_elem:
                        title_link = title_elem.find('a')
                        title = title_link.get_text(strip=True) if title_link else 'N/A'
                        job_url = urljoin('https://in.indeed.com', title_link['href']) if title_link else ''
                    else:
                        continue
                    
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    
                    location_elem = card.find('div', class_='companyLocation')
                    location_text = location_elem.get_text(strip=True) if location_elem else 'N/A'
                    
                    salary_elem = card.find('span', class_='salaryText')
                    salary = salary_elem.get_text(strip=True) if salary_elem else 'Not disclosed'
                    
                    posted_elem = card.find('span', class_='date')
                    posted_text = posted_elem.get_text(strip=True) if posted_elem else 'Recently'
                    posted_date = self.parse_posted_date(posted_text)
                    
                    desc_elem = card.find('div', class_='summary')
                    description = desc_elem.get_text(strip=True) if desc_elem else 'No description available'
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'job_type': 'Full-time',
                        'experience_required': 'Not specified',
                        'salary_range': salary,
                        'description': description[:500],
                        'job_url': job_url,
                        'posted_date': posted_date,
                        'portal': 'Indeed.com'
                    })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        
        return jobs

    def scrape_linkedin(self, query, location, max_jobs=5):
        jobs = []
        try:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(query)}"
            if location:
                search_url += f"&location={quote_plus(location)}"
            
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='base-card')[:max_jobs]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                    
                    link_elem = card.find('a', class_='base-card__full-link')
                    job_url = link_elem['href'] if link_elem else ''
                    
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    
                    location_elem = card.find('span', class_='job-search-card__location')
                    location_text = location_elem.get_text(strip=True) if location_elem else 'N/A'
                    
                    posted_elem = card.find('time', class_='job-search-card__listdate')
                    posted_text = posted_elem.get_text(strip=True) if posted_elem else 'Recently'
                    posted_date = self.parse_posted_date(posted_text)
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'job_type': 'Full-time',
                        'experience_required': 'Not specified',
                        'salary_range': 'Not disclosed',
                        'description': 'Click to view full job description',
                        'job_url': job_url,
                        'posted_date': posted_date,
                        'portal': 'LinkedIn Jobs'
                    })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
        
        return jobs

    def scrape_monster(self, query, location, max_jobs=5):
        jobs = []
        try:
            search_url = f"https://www.monster.com/jobs/search/?q={quote_plus(query)}"
            if location:
                search_url += f"&where={quote_plus(location)}"
            
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('section', class_='card-content')[:max_jobs]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='title')
                    if title_elem:
                        title_link = title_elem.find('a')
                        title = title_link.get_text(strip=True) if title_link else 'N/A'
                        job_url = urljoin('https://www.monster.com', title_link['href']) if title_link else ''
                    else:
                        continue
                    
                    company_elem = card.find('div', class_='company')
                    company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                    
                    location_elem = card.find('div', class_='location')
                    location_text = location_elem.get_text(strip=True) if location_elem else 'N/A'
                    
                    posted_elem = card.find('div', class_='meta')
                    posted_text = posted_elem.get_text(strip=True) if posted_elem else 'Recently'
                    posted_date = self.parse_posted_date(posted_text)
                    
                    desc_elem = card.find('div', class_='summary')
                    description = desc_elem.get_text(strip=True) if desc_elem else 'No description available'
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'job_type': 'Full-time',
                        'experience_required': 'Not specified',
                        'salary_range': 'Not disclosed',
                        'description': description[:500],
                        'job_url': job_url,
                        'posted_date': posted_date,
                        'portal': 'Monster.com'
                    })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping Monster: {e}")
        
        return jobs

    def parse_posted_date(self, posted_text):
        """Parse posted date from various formats"""
        now = datetime.now()
        posted_text = posted_text.lower().strip()
        
        if 'today' in posted_text or 'just now' in posted_text:
            return now
        elif 'yesterday' in posted_text:
            return now - timedelta(days=1)
        elif 'hour' in posted_text:
            hours = re.findall(r'\d+', posted_text)
            if hours:
                return now - timedelta(hours=int(hours[0]))
        elif 'day' in posted_text:
            days = re.findall(r'\d+', posted_text)
            if days:
                return now - timedelta(days=int(days[0]))
        elif 'week' in posted_text:
            weeks = re.findall(r'\d+', posted_text)
            if weeks:
                return now - timedelta(weeks=int(weeks[0]))
        
        return now

    def scrape_all_portals_real(self, query, location='', max_jobs_per_portal=10):
        """Scrape jobs from all portals in real-time with progress tracking"""
        results = {
            'naukri': [],
            'indeed': [],
            'linkedin': [],
            'monster': []
        }
        
        portals = [
            ('naukri', self.scrape_naukri),
            ('indeed', self.scrape_indeed),
            ('linkedin', self.scrape_linkedin),
            ('monster', self.scrape_monster)
        ]
        
        for portal_name, scraper_func in portals:
            try:
                jobs = scraper_func(query, location, max_jobs_per_portal)
                # Filter jobs posted within 1 day
                recent_jobs = [job for job in jobs if self.is_recent_job(job['posted_date'])]
                results[portal_name] = recent_jobs
                time.sleep(random.uniform(1, 2))
            except Exception as e:
                print(f"Error scraping {portal_name}: {e}")
                results[portal_name] = []
        
        return results
    
    def is_recent_job(self, posted_date):
        """Check if job was posted within 1 day"""
        now = datetime.now()
        time_diff = now - posted_date
        return time_diff.days <= 1