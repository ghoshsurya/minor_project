from django.core.management.base import BaseCommand
from job_scraper.models import JobListing, JobPortal
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create sample job listings'

    def handle(self, *args, **options):
        # Create job portals first
        portals_data = [
            {'name': 'Naukri.com', 'base_url': 'https://naukri.com', 'is_active': True},
            {'name': 'Indeed.com', 'base_url': 'https://indeed.com', 'is_active': True},
            {'name': 'LinkedIn Jobs', 'base_url': 'https://linkedin.com/jobs', 'is_active': True},
            {'name': 'Monster.com', 'base_url': 'https://monster.com', 'is_active': True},
        ]
        
        for portal_data in portals_data:
            portal, created = JobPortal.objects.get_or_create(
                name=portal_data['name'],
                defaults=portal_data
            )
            if created:
                self.stdout.write(f'Created portal: {portal.name}')

        # Sample job data
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'company': 'TechCorp Solutions',
                'location': 'Bangalore, Karnataka',
                'job_type': 'full-time',
                'experience_required': '3-5 years',
                'salary_range': '₹8-15 LPA',
                'description': 'We are looking for a Senior Python Developer to join our team. Experience with Django, Flask, and REST APIs required.',
                'requirements': 'Python, Django, Flask, REST API, PostgreSQL, Git',
            },
            {
                'title': 'Frontend React Developer',
                'company': 'WebTech Innovations',
                'location': 'Mumbai, Maharashtra',
                'job_type': 'full-time',
                'experience_required': '2-4 years',
                'salary_range': '₹6-12 LPA',
                'description': 'Join our frontend team to build amazing user interfaces using React.js and modern web technologies.',
                'requirements': 'React.js, JavaScript, HTML, CSS, Redux, Git',
            },
            {
                'title': 'Data Scientist',
                'company': 'Analytics Pro',
                'location': 'Hyderabad, Telangana',
                'job_type': 'full-time',
                'experience_required': '2-6 years',
                'salary_range': '₹10-20 LPA',
                'description': 'Seeking a Data Scientist to work on machine learning projects and data analysis.',
                'requirements': 'Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL',
            },
            {
                'title': 'DevOps Engineer',
                'company': 'CloudTech Systems',
                'location': 'Pune, Maharashtra',
                'job_type': 'full-time',
                'experience_required': '3-7 years',
                'salary_range': '₹12-22 LPA',
                'description': 'Looking for DevOps Engineer to manage cloud infrastructure and CI/CD pipelines.',
                'requirements': 'AWS, Docker, Kubernetes, Jenkins, Terraform, Linux',
            },
            {
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'location': 'Delhi, NCR',
                'job_type': 'full-time',
                'experience_required': '1-3 years',
                'salary_range': '₹5-10 LPA',
                'description': 'Join our startup as a Full Stack Developer working with modern web technologies.',
                'requirements': 'JavaScript, Node.js, React, MongoDB, Express.js',
            },
            {
                'title': 'UI/UX Designer',
                'company': 'Design Studio',
                'location': 'Chennai, Tamil Nadu',
                'job_type': 'full-time',
                'experience_required': '2-5 years',
                'salary_range': '₹4-8 LPA',
                'description': 'Creative UI/UX Designer needed to design user-friendly interfaces and experiences.',
                'requirements': 'Figma, Adobe XD, Photoshop, Illustrator, Prototyping',
            },
            {
                'title': 'Java Backend Developer',
                'company': 'Enterprise Solutions',
                'location': 'Kolkata, West Bengal',
                'job_type': 'full-time',
                'experience_required': '3-6 years',
                'salary_range': '₹7-14 LPA',
                'description': 'Java Backend Developer for enterprise applications using Spring Boot and microservices.',
                'requirements': 'Java, Spring Boot, Microservices, MySQL, REST API',
            },
            {
                'title': 'Mobile App Developer',
                'company': 'MobileTech',
                'location': 'Ahmedabad, Gujarat',
                'job_type': 'full-time',
                'experience_required': '2-4 years',
                'salary_range': '₹6-11 LPA',
                'description': 'Develop mobile applications for iOS and Android platforms using React Native.',
                'requirements': 'React Native, JavaScript, iOS, Android, Firebase',
            },
            {
                'title': 'Digital Marketing Specialist',
                'company': 'Marketing Hub',
                'location': 'Jaipur, Rajasthan',
                'job_type': 'full-time',
                'experience_required': '1-3 years',
                'salary_range': '₹3-6 LPA',
                'description': 'Digital Marketing Specialist to manage online campaigns and social media marketing.',
                'requirements': 'SEO, SEM, Google Analytics, Social Media, Content Marketing',
            },
            {
                'title': 'Product Manager',
                'company': 'ProductCorp',
                'location': 'Gurgaon, Haryana',
                'job_type': 'full-time',
                'experience_required': '4-8 years',
                'salary_range': '₹15-25 LPA',
                'description': 'Product Manager to lead product development and strategy for our SaaS platform.',
                'requirements': 'Product Management, Agile, Scrum, Analytics, Strategy',
            }
        ]

        portals = list(JobPortal.objects.all())
        
        for job_data in jobs_data:
            # Random portal and recent date
            portal = random.choice(portals)
            posted_date = timezone.now() - timedelta(days=random.randint(0, 7))
            
            job, created = JobListing.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults={
                    'location': job_data['location'],
                    'job_type': job_data['job_type'],
                    'experience_required': job_data['experience_required'],
                    'salary_range': job_data['salary_range'],
                    'description': job_data['description'],
                    'portal': portal,
                    'posted_date': posted_date,
                    'job_url': f'{portal.base_url}/job/{job_data["title"].lower().replace(" ", "-")}',
                    'is_recent': True
                }
            )
            
            if created:
                self.stdout.write(f'Created job: {job.title} at {job.company}')
            else:
                self.stdout.write(f'Job already exists: {job.title} at {job.company}')

        self.stdout.write(self.style.SUCCESS('Sample jobs created successfully!'))