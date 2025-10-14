from django.core.management.base import BaseCommand
from cv_optimizer.models import CVTemplate

class Command(BaseCommand):
    help = 'Create sample CV templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Modern Professional',
                'template_type': 'modern',
                'description': 'Clean and modern design perfect for tech and creative roles',
                'html_template': '<div>Modern Template</div>',
                'css_styles': 'body { font-family: Arial; }',
                'is_active': True
            },
            {
                'name': 'Classic Executive',
                'template_type': 'classic',
                'description': 'Traditional format ideal for corporate and executive positions',
                'html_template': '<div>Classic Template</div>',
                'css_styles': 'body { font-family: Times; }',
                'is_active': True
            },
            {
                'name': 'Creative Designer',
                'template_type': 'creative',
                'description': 'Eye-catching design for creative professionals and designers',
                'html_template': '<div>Creative Template</div>',
                'css_styles': 'body { font-family: Helvetica; }',
                'is_active': True
            },
            {
                'name': 'Minimal Clean',
                'template_type': 'minimal',
                'description': 'Simple and clean layout focusing on content',
                'html_template': '<div>Minimal Template</div>',
                'css_styles': 'body { font-family: Calibri; }',
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

        self.stdout.write(self.style.SUCCESS('CV Templates setup complete!'))