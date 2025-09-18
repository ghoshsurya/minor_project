import os
import re
import nltk
from collections import Counter
from PyPDF2 import PdfReader
from docx import Document
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"

def get_job_keywords(job_role):
    """Get relevant keywords for a job role"""
    job_keywords = {
        'software developer': [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'git', 'agile',
            'api', 'database', 'frontend', 'backend', 'full-stack', 'programming',
            'software development', 'web development', 'mobile development'
        ],
        'data scientist': [
            'python', 'r', 'machine learning', 'deep learning', 'statistics', 'sql',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'data analysis',
            'data visualization', 'big data', 'hadoop', 'spark', 'tableau', 'power bi'
        ],
        'marketing manager': [
            'digital marketing', 'seo', 'sem', 'social media', 'content marketing',
            'email marketing', 'analytics', 'google analytics', 'campaign management',
            'brand management', 'market research', 'lead generation', 'roi', 'kpi'
        ],
        'project manager': [
            'project management', 'agile', 'scrum', 'pmp', 'risk management',
            'stakeholder management', 'budget management', 'timeline management',
            'team leadership', 'communication', 'planning', 'execution', 'monitoring'
        ]
    }
    
    # Default keywords for any job
    default_keywords = [
        'experience', 'skills', 'education', 'certification', 'leadership',
        'teamwork', 'communication', 'problem solving', 'analytical', 'creative'
    ]
    
    job_role_lower = job_role.lower()
    for role, keywords in job_keywords.items():
        if role in job_role_lower:
            return keywords + default_keywords
    
    return default_keywords

def calculate_ats_score(cv_text, job_keywords):
    """Calculate ATS score based on keyword matching"""
    cv_text_lower = cv_text.lower()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    cv_words = [word for word in word_tokenize(cv_text_lower) if word.isalnum() and word not in stop_words]
    
    # Count keyword matches
    keyword_matches = 0
    matched_keywords = []
    
    for keyword in job_keywords:
        if keyword.lower() in cv_text_lower:
            keyword_matches += 1
            matched_keywords.append(keyword)
    
    # Calculate score (0-100)
    score = min((keyword_matches / len(job_keywords)) * 100, 100)
    
    return {
        'score': round(score, 2),
        'matched_keywords': matched_keywords,
        'total_keywords': len(job_keywords),
        'missing_keywords': [kw for kw in job_keywords if kw.lower() not in cv_text_lower]
    }

def analyze_cv_structure(cv_text):
    """Analyze CV structure and format"""
    analysis = {
        'has_contact_info': bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cv_text)),
        'has_phone': bool(re.search(r'[\+]?[1-9]?[0-9]{7,14}', cv_text)),
        'has_experience_section': any(word in cv_text.lower() for word in ['experience', 'work history', 'employment']),
        'has_education_section': any(word in cv_text.lower() for word in ['education', 'qualification', 'degree']),
        'has_skills_section': any(word in cv_text.lower() for word in ['skills', 'technical skills', 'competencies']),
        'word_count': len(cv_text.split()),
        'has_bullet_points': '•' in cv_text or '*' in cv_text or '-' in cv_text
    }
    
    return analysis

def analyze_cv(file_path, job_role):
    """Main function to analyze CV"""
    # Extract text from CV
    cv_text = extract_text_from_file(file_path)
    
    if cv_text.startswith("Error"):
        return {
            'score': 0,
            'error': cv_text,
            'suggestions': ['Please upload a valid PDF or DOCX file.']
        }
    
    # Get job-specific keywords
    job_keywords = get_job_keywords(job_role)
    
    # Calculate ATS score
    score_analysis = calculate_ats_score(cv_text, job_keywords)
    
    # Analyze CV structure
    structure_analysis = analyze_cv_structure(cv_text)
    
    # Generate suggestions
    suggestions = generate_suggestions(score_analysis, structure_analysis)
    
    return {
        'score': score_analysis['score'],
        'matched_keywords': score_analysis['matched_keywords'],
        'missing_keywords': score_analysis['missing_keywords'],
        'structure_analysis': structure_analysis,
        'suggestions': suggestions,
        'job_role': job_role
    }

def generate_suggestions(score_analysis, structure_analysis):
    """Generate improvement suggestions"""
    suggestions = []
    
    # Score-based suggestions
    if score_analysis['score'] < 30:
        suggestions.append("Your CV has a low ATS score. Consider adding more relevant keywords.")
    elif score_analysis['score'] < 60:
        suggestions.append("Your CV has a moderate ATS score. Add missing keywords to improve.")
    else:
        suggestions.append("Great! Your CV has a good ATS score.")
    
    # Structure-based suggestions
    if not structure_analysis['has_contact_info']:
        suggestions.append("Add your email address for better contact information.")
    
    if not structure_analysis['has_phone']:
        suggestions.append("Include your phone number in the contact section.")
    
    if not structure_analysis['has_experience_section']:
        suggestions.append("Add a clear 'Work Experience' or 'Professional Experience' section.")
    
    if not structure_analysis['has_education_section']:
        suggestions.append("Include an 'Education' section with your qualifications.")
    
    if not structure_analysis['has_skills_section']:
        suggestions.append("Add a 'Skills' section highlighting your technical and soft skills.")
    
    if structure_analysis['word_count'] < 200:
        suggestions.append("Your CV seems too short. Consider adding more details about your experience.")
    elif structure_analysis['word_count'] > 800:
        suggestions.append("Your CV might be too long. Consider condensing the content.")
    
    if not structure_analysis['has_bullet_points']:
        suggestions.append("Use bullet points to make your CV more readable and ATS-friendly.")
    
    # Missing keywords suggestions
    if score_analysis['missing_keywords']:
        missing_kw = ', '.join(score_analysis['missing_keywords'][:5])
        suggestions.append(f"Consider adding these relevant keywords: {missing_kw}")
    
    return suggestions

def optimize_cv(file_path, analysis_report):
    """Generate optimized CV suggestions"""
    # This is a simplified version - in a real implementation,
    # you would use more sophisticated NLP and document generation
    
    optimization_tips = {
        'format': [
            "Use a clean, professional format",
            "Ensure consistent font and spacing",
            "Use bullet points for easy scanning",
            "Keep margins between 0.5-1 inch"
        ],
        'content': [
            "Start with a strong professional summary",
            "Use action verbs to describe achievements",
            "Quantify your accomplishments with numbers",
            "Tailor content to the specific job role"
        ],
        'keywords': [
            f"Include these missing keywords: {', '.join(analysis_report.get('missing_keywords', [])[:10])}",
            "Use industry-specific terminology",
            "Include both hard and soft skills",
            "Match keywords from the job description"
        ]
    }
    
    return optimization_tips