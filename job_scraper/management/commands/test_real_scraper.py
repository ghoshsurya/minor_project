from django.core.management.base import BaseCommand
from job_scraper.real_scraper import RealJobScraper

class Command(BaseCommand):
    help = 'Test real job scraper'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='python developer', help='Job search query')
        parser.add_argument('--location', type=str, default='', help='Job location')

    def handle(self, *args, **options):
        query = options['query']
        location = options['location']
        
        self.stdout.write(f'Testing real scraper for: {query} in {location or "All India"}')
        
        scraper = RealJobScraper()
        jobs = scraper.scrape_all_portals_real(query, location, 2)
        
        self.stdout.write(f'Found {len(jobs)} jobs:')
        
        for job in jobs:
            self.stdout.write(f"\nPortal: {job['portal']}")
            self.stdout.write(f"Title: {job['title']}")
            self.stdout.write(f"Company: {job['company']}")
            self.stdout.write(f"Location: {job['location']}")
            self.stdout.write(f"URL: {job['job_url']}")
            self.stdout.write("-" * 50)
        
        self.stdout.write(self.style.SUCCESS('Real scraper test completed!'))