import os
import tempfile
import subprocess
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time

def compile_latex_to_pdf(latex_code, user_id):
    """Compile LaTeX code to PDF with fallback"""
    try:
        # Try LaTeX compilation first
        return compile_with_latex(latex_code, user_id)
    except:
        # Fallback to simple PDF generation
        return compile_with_reportlab(latex_code, user_id)

def compile_with_latex(latex_code, user_id):
    """Compile using pdflatex"""
    temp_dir = tempfile.mkdtemp()
    tex_path = os.path.join(temp_dir, 'document.tex')
    
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    
    result = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_path],
        capture_output=True, text=True, timeout=30
    )
    
    pdf_path = os.path.join(temp_dir, 'document.pdf')
    
    if os.path.exists(pdf_path):
        # Move to media directory
        media_path = os.path.join(settings.MEDIA_ROOT, 'latex_pdfs')
        os.makedirs(media_path, exist_ok=True)
        
        timestamp = int(time.time())
        final_pdf = os.path.join(media_path, f'cv_{user_id}_{timestamp}.pdf')
        
        import shutil
        shutil.copy2(pdf_path, final_pdf)
        shutil.rmtree(temp_dir)
        
        return f'/media/latex_pdfs/cv_{user_id}_{timestamp}.pdf'
    else:
        raise Exception("LaTeX compilation failed")

def compile_with_reportlab(latex_code, user_id):
    """Fallback PDF generation using reportlab"""
    # Clean LaTeX code to extract text
    import re
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', latex_code)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = text.replace('{', '').replace('}', '')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Create PDF
    media_path = os.path.join(settings.MEDIA_ROOT, 'latex_pdfs')
    os.makedirs(media_path, exist_ok=True)
    
    timestamp = int(time.time())
    pdf_path = os.path.join(media_path, f'cv_{user_id}_{timestamp}.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    y = 750
    
    for line in lines[:40]:
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(50, y, line[:80])
        y -= 20
    
    c.save()
    return f'/media/latex_pdfs/cv_{user_id}_{timestamp}.pdf'