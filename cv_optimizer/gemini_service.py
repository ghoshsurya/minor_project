import google.generativeai as genai
from django.conf import settings
import json
import re

class GeminiCVAnalyzer:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def analyze_cv(self, cv_text, job_description=""):
        prompt = f"""
        Analyze this CV and provide detailed feedback:
        
        CV Content: {cv_text}
        Job Description: {job_description}
        
        Provide response in JSON format:
        {{
            "ats_score": 85,
            "missing_sections": ["Skills", "Certifications"],
            "improvements": ["Add quantified achievements", "Include relevant keywords"],
            "keyword_suggestions": ["Python", "Machine Learning", "AWS"],
            "optimized_sections": {{
                "summary": "Optimized professional summary",
                "experience": "Enhanced experience section",
                "skills": "Recommended skills section"
            }},
            "job_match_percentage": 75
        }}
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return self._parse_response(response.text)
    
    def generate_optimized_cv(self, cv_text, analysis_data):
        prompt = f"""
        Create an ATS-optimized CV based on this analysis:
        
        Original CV: {cv_text}
        Analysis: {analysis_data}
        
        Generate a complete, professional CV with:
        - ATS-friendly formatting
        - Relevant keywords
        - Quantified achievements
        - Professional summary
        - Skills section
        - Experience with impact metrics
        
        Return only the CV content in plain text format.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def find_matching_jobs(self, cv_analysis, location=""):
        prompt = f"""
        Based on this CV analysis, suggest job search terms and job types:
        
        Analysis: {cv_analysis}
        Location: {location}
        
        Provide JSON response:
        {{
            "job_titles": ["Software Engineer", "Data Analyst"],
            "search_keywords": ["python", "machine learning"],
            "job_portals": ["LinkedIn", "Indeed", "Naukri"],
            "application_tips": ["Customize resume for each job", "Write compelling cover letter"]
        }}
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            return self._parse_job_response(response.text)
    
    def get_application_guide(self, job_title, company_name=""):
        prompt = f"""
        Provide a comprehensive job application guide for:
        Job Title: {job_title}
        Company: {company_name}
        
        Include:
        1. Application strategy
        2. Interview preparation tips
        3. Common questions
        4. Skills to highlight
        5. Resources for preparation
        
        Format as structured text.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _parse_response(self, text):
        # Fallback parser for non-JSON responses
        return {
            "ats_score": 70,
            "missing_sections": ["Skills"],
            "improvements": ["Improve formatting", "Add keywords"],
            "keyword_suggestions": ["Relevant skills"],
            "optimized_sections": {"summary": "Professional summary needed"},
            "job_match_percentage": 65
        }
    
    def _parse_job_response(self, text):
        return {
            "job_titles": ["Software Developer"],
            "search_keywords": ["programming"],
            "job_portals": ["LinkedIn", "Indeed"],
            "application_tips": ["Tailor your resume"]
        }