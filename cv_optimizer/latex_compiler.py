from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import os
import time
from django.conf import settings

class CompileLaTeXView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            latex_code = data.get('latex', '')
            
            if not latex_code.strip():
                return JsonResponse({'success': False, 'error': 'No LaTeX code provided'})
            
            # Simple PDF generation using reportlab
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            # Clean LaTeX code properly
            import re
            # Remove comments
            text = re.sub(r'%.*', '', latex_code)
            # Extract content between \begin{document} and \end{document}
            doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', text, re.DOTALL)
            if doc_match:
                text = doc_match.group(1)
            
            # Clean LaTeX commands
            text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
            text = re.sub(r'\\[a-zA-Z]+', '', text)
            text = text.replace('{', '').replace('}', '').replace('\\', '')
            lines = [line.strip() for line in text.split('\n') if line.strip() and not line.startswith('%')]
            
            # Create PDF
            media_path = os.path.join(settings.MEDIA_ROOT, 'latex_pdfs')
            os.makedirs(media_path, exist_ok=True)
            
            timestamp = int(time.time())
            pdf_path = os.path.join(media_path, f'cv_{request.user.id}_{timestamp}.pdf')
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            y = height - 50
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, "CV Document")
            y -= 40
            
            c.setFont("Helvetica", 12)
            for line in lines[:35]:
                if y < 50:
                    c.showPage()
                    y = height - 50
                # Handle long lines
                if len(line) > 70:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 70:
                            current_line += word + " "
                        else:
                            c.drawString(50, y, current_line.strip())
                            y -= 15
                            current_line = word + " "
                    if current_line:
                        c.drawString(50, y, current_line.strip())
                        y -= 15
                else:
                    c.drawString(50, y, line)
                    y -= 15
            
            c.save()
            
            pdf_url = f'/media/latex_pdfs/cv_{request.user.id}_{timestamp}.pdf'
            return JsonResponse({'success': True, 'pdf_url': pdf_url})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})