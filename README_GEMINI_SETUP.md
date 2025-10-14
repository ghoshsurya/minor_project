# Gemini AI Integration Setup Guide

## Overview
Your ATS CV Optimizer now includes advanced AI automation using Google's Gemini API. This integration provides:

- **AI-Powered CV Analysis**: Deep analysis of CV content with personalized suggestions
- **Automated CV Optimization**: Generate ATS-friendly optimized CVs
- **Smart Job Matching**: Find relevant jobs based on CV analysis
- **Application Guidance**: Get detailed application strategies for specific jobs
- **Job Portal Integration**: Direct links to job applications with portal-specific tips

## Setup Instructions

### 1. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 2. Configure Environment
1. Open `.env` file in the project root
2. Replace `your-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 3. New Features Available

#### AI CV Analysis
- Upload CV → Get AI-powered analysis
- ATS score calculation
- Missing sections identification
- Keyword suggestions
- Job match percentage

#### Optimized CV Generation
- AI generates optimized CV content
- Download as PDF
- ATS-friendly formatting
- Industry-specific keywords

#### Smart Job Matching
- Find jobs matching your CV
- Multiple job portal integration
- Location-based filtering
- Application difficulty assessment

#### Application Guide
- AI-generated application strategies
- Portal-specific tips (LinkedIn, Indeed, Naukri, etc.)
- Interview preparation resources
- Learning resources and certifications

### 4. New URLs Available

```
/cv-optimizer/ai-optimized/<cv_id>/          # AI analysis results
/cv-optimizer/ai-download/<cv_id>/           # Download optimized CV
/cv-optimizer/job-matching/<cv_id>/          # Find matching jobs
/cv-optimizer/application-guide/             # Job application guide
/cv-optimizer/regenerate-analysis/<cv_id>/   # Regenerate AI analysis
```

### 5. Usage Workflow

1. **Upload CV**: Use existing upload form
2. **AI Analysis**: Automatic analysis with Gemini AI
3. **View Results**: See detailed analysis and suggestions
4. **Download Optimized CV**: Get AI-optimized version
5. **Find Jobs**: Search for matching opportunities
6. **Application Guide**: Get specific application strategies
7. **Apply**: Direct links to job portals

### 6. Features Added

#### Backend Services
- `GeminiCVAnalyzer`: Core AI analysis service
- `JobMatcher`: Job matching and portal integration
- Enhanced models with AI analysis fields
- PDF generation from AI-optimized content

#### Frontend Templates
- AI analysis dashboard
- Job matching interface
- Application guide with resources
- Interactive checklists and progress tracking

#### Database Changes
- New fields for AI analysis results
- Job match percentages
- Optimized content storage
- Keyword suggestions storage

### 7. Error Handling
- Graceful fallback if API key is missing
- Error messages for failed AI requests
- Offline mode with basic analysis
- Retry mechanisms for API failures

### 8. Performance Considerations
- AI analysis runs asynchronously
- Results cached in database
- Regeneration option available
- Optimized API calls

## Testing the Integration

1. Start the server: `py manage.py runserver`
2. Upload a CV through the web interface
3. Check the AI analysis results
4. Test job matching functionality
5. Try the application guide features

## Troubleshooting

### Common Issues
1. **API Key Error**: Ensure GEMINI_API_KEY is set correctly in .env
2. **Import Errors**: Run `pip install google-generativeai reportlab`
3. **Migration Issues**: Run `py manage.py migrate`
4. **Template Errors**: Check template paths and context variables

### Support
- Check Django logs for detailed error messages
- Verify API key permissions in Google AI Studio
- Ensure all dependencies are installed
- Test with a simple CV first

## Next Steps
- Customize AI prompts for your specific needs
- Add more job portals to the scraping service
- Implement real-time job alerts
- Add more detailed analytics and reporting