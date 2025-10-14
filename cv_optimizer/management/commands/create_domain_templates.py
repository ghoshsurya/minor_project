from django.core.management.base import BaseCommand
from cv_optimizer.models import CVTemplate

class Command(BaseCommand):
    help = 'Create domain-specific CV templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Web Developer Pro',
                'template_type': 'modern',
                'description': 'Perfect for frontend and fullstack web developers showcasing projects and technical skills',
                'html_template': '<div>Web Developer Template</div>',
                'css_styles': 'body { font-family: "Roboto", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'Data Analyst Expert',
                'template_type': 'professional',
                'description': 'Ideal for data analysts highlighting analytical skills and data visualization experience',
                'html_template': '<div>Data Analyst Template</div>',
                'css_styles': 'body { font-family: "Open Sans", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'Mobile Developer',
                'template_type': 'modern',
                'description': 'Designed for iOS and Android developers with focus on app development portfolio',
                'html_template': '<div>Mobile Developer Template</div>',
                'css_styles': 'body { font-family: "Poppins", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'DevOps Engineer',
                'template_type': 'professional',
                'description': 'Technical template for DevOps professionals emphasizing infrastructure and automation',
                'html_template': '<div>DevOps Template</div>',
                'css_styles': 'body { font-family: "Source Code Pro", monospace; }',
                'is_active': True
            },
            {
                'name': 'UI/UX Designer',
                'template_type': 'creative',
                'description': 'Creative layout for designers showcasing visual design skills and portfolio',
                'html_template': '<div>UI/UX Designer Template</div>',
                'css_styles': 'body { font-family: "Nunito", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'Digital Marketer',
                'template_type': 'modern',
                'description': 'Marketing-focused template highlighting campaigns, analytics, and growth metrics',
                'html_template': '<div>Digital Marketer Template</div>',
                'css_styles': 'body { font-family: "Lato", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'Product Manager',
                'template_type': 'professional',
                'description': 'Executive template for product managers showcasing leadership and strategic thinking',
                'html_template': '<div>Product Manager Template</div>',
                'css_styles': 'body { font-family: "Merriweather", serif; }',
                'is_active': True
            },
            {
                'name': 'Cybersecurity Specialist',
                'template_type': 'professional',
                'description': 'Security-focused template for cybersecurity professionals and ethical hackers',
                'html_template': '<div>Cybersecurity Template</div>',
                'css_styles': 'body { font-family: "Fira Code", monospace; }',
                'is_active': True
            },
            {
                'name': 'Machine Learning Engineer',
                'template_type': 'modern',
                'description': 'AI/ML focused template for data scientists and machine learning engineers',
                'html_template': '<div>ML Engineer Template</div>',
                'css_styles': 'body { font-family: "Inter", sans-serif; }',
                'is_active': True
            },
            {
                'name': 'Sales Professional',
                'template_type': 'classic',
                'description': 'Results-driven template for sales professionals highlighting achievements and targets',
                'html_template': '<div>Sales Professional Template</div>',
                'css_styles': 'body { font-family: "Playfair Display", serif; }',
                'is_active': True
            }
        ]

        for template_data in templates:
            template, created = CVTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created template: {template.name}')
            else:
                self.stdout.write(f'Template already exists: {template.name}')

        self.stdout.write(self.style.SUCCESS('Domain-specific templates created successfully!'))