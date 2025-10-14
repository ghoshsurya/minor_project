from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json

class CompileLaTeXView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            latex_code = data.get('latex', '')
            
            if not latex_code.strip():
                return JsonResponse({'success': False, 'error': 'No LaTeX code provided'})
            
            from .pdf_generator import generate_cv_pdf
            
            pdf_url = generate_cv_pdf(latex_code, request.user.id)
            return JsonResponse({'success': True, 'pdf_url': pdf_url})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})