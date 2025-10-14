from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re
import os
import time
from django.conf import settings

def generate_cv_pdf(latex_code, user_id):
    """Generate a proper CV PDF from LaTeX code"""
    
    # Create PDF path
    media_path = os.path.join(settings.MEDIA_ROOT, 'latex_pdfs')
    os.makedirs(media_path, exist_ok=True)
    
    timestamp = int(time.time())
    pdf_path = os.path.join(media_path, f'cv_{user_id}_{timestamp}.pdf')
    
    # Extract CV information
    name_match = re.search(r'\\name\{([^}]*)\}', latex_code)
    tagline_match = re.search(r'\\tagline\{([^}]*)\}', latex_code)
    email_match = re.search(r'\\email\{([^}]*)\}', latex_code)
    phone_match = re.search(r'\\phone\{([^}]*)\}', latex_code)
    
    name = name_match.group(1) if name_match else "Your Name"
    tagline = tagline_match.group(1) if tagline_match else "Your Position"
    email = email_match.group(1) if email_match else ""
    phone = phone_match.group(1) if phone_match else ""
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph(f'<para align="center"><b><font size="20">{name}</font></b></para>', styles['Normal']))
    story.append(Paragraph(f'<para align="center"><i><font size="14">{tagline}</font></i></para>', styles['Normal']))
    
    if email or phone:
        contact = f'<para align="center">{email} | {phone}</para>'
        story.append(Paragraph(contact, styles['Normal']))
    
    story.append(Spacer(1, 30))
    
    # Extract sections
    sections = re.findall(r'\\cvsection\{([^}]*)\}(.*?)(?=\\cvsection|\\end\{document\}|$)', latex_code, re.DOTALL)
    
    for section_title, section_content in sections:
        # Section header
        story.append(Paragraph(f'<b><font size="16">{section_title.upper()}</font></b>', styles['Heading1']))
        story.append(Spacer(1, 10))
        
        # Extract events
        events = re.findall(r'\\cvevent\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}', section_content)
        
        for title, company, date, location in events:
            story.append(Paragraph(f'<b>{title}</b>', styles['Normal']))
            story.append(Paragraph(f'{company} | {date} | {location}', styles['Normal']))
            
            # Extract bullet points
            bullets = re.findall(r'\\item\s+([^\n\\]*)', section_content)
            for bullet in bullets:
                story.append(Paragraph(f'• {bullet}', styles['Normal']))
            
            story.append(Spacer(1, 10))
        
        # Handle other content
        clean_content = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', section_content)
        clean_content = re.sub(r'\\[a-zA-Z]+', '', clean_content)
        lines = [line.strip() for line in clean_content.split('\n') if line.strip()]
        
        for line in lines:
            if line and not line.startswith('\\'):
                story.append(Paragraph(line, styles['Normal']))
        
        story.append(Spacer(1, 20))
    
    doc.build(story)
    return f'/media/latex_pdfs/cv_{user_id}_{timestamp}.pdf'