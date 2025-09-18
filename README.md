# ATS-Friendly CV Optimizer and Smart Job Hunting Assistant

A comprehensive Django web application that helps job seekers optimize their CVs for Applicant Tracking Systems (ATS) and find relevant job opportunities.

## Team Members
- Uttam Kumar Mahto (Roll No. 15571024001)
- Suryakant Ghosh (Roll No. 15571024020)
- Jiten Paramanik (Roll No. 15571024019)
- Subhadeep Gorai (Roll No. 15571024018)

## Features

### 🔍 CV Analysis & Optimization
- Upload CV in PDF, DOC, or DOCX format
- Get detailed ATS compatibility score
- Receive personalized improvement suggestions
- Download optimized ATS-friendly CV

### 💼 Smart Job Search
- Search jobs from multiple portals
- Filter by location, job type, and experience
- Get job recommendations based on profile
- Set up job alerts for matching opportunities

### 📊 Dashboard & Analytics
- Track CV performance over time
- View analysis history
- Monitor improvement progress
- Quick access to all features

### 🎯 Additional Features
- Dark/Light theme toggle
- Responsive design for all devices
- Modern admin panel
- Interview preparation resources
- User authentication & profiles

## Technology Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (can be switched to PostgreSQL)
- **Celery** - Background tasks
- **Redis** - Caching and message broker

### Frontend
- **Bootstrap 5.3** - CSS framework
- **JavaScript (ES6+)** - Interactive features
- **Font Awesome** - Icons
- **Google Fonts** - Typography

### CV Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **NLTK** - Natural language processing
- **BeautifulSoup** - Web scraping

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "MINOR PROJECT"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Project Structure

```
MINOR PROJECT/
├── ats_optimizer/          # Main project settings
├── accounts/               # User authentication & profiles
├── cv_optimizer/           # CV analysis & optimization
├── job_scraper/           # Job search & scraping
├── core/                  # Core functionality & pages
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── media/                # User uploaded files
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## Key Functionalities

### CV Analysis Process
1. **Text Extraction**: Extract text from uploaded CV files
2. **Keyword Matching**: Compare CV content with job-specific keywords
3. **Structure Analysis**: Check for essential CV sections
4. **Score Calculation**: Generate ATS compatibility score (0-100%)
5. **Suggestions**: Provide actionable improvement recommendations

### Job Scraping
- Scrapes job listings from popular job portals
- Filters recent jobs (within last 24 hours)
- Stores job data with company, location, and requirements
- Provides job recommendations based on user profile

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Mode**: Toggle between themes
- **Drag & Drop**: Easy file upload interface
- **Real-time Updates**: AJAX-powered interactions
- **Progressive Enhancement**: Works without JavaScript

## Admin Panel Features

Access the admin panel at `/admin/` with superuser credentials:

- **User Management**: View and manage user accounts
- **CV Analytics**: Monitor CV uploads and scores
- **Job Management**: Manage job listings and portals
- **Content Management**: Update resources and messages
- **System Monitoring**: Track application usage

## API Endpoints

The application provides REST API endpoints for:
- CV upload and analysis
- Job search and filtering
- User profile management
- Job alerts and notifications

## Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **File Validation**: Secure file upload with type and size validation
- **User Authentication**: Secure login/logout functionality
- **Permission Control**: Role-based access control
- **Data Sanitization**: Input validation and sanitization

## Performance Optimizations

- **Static File Compression**: Whitenoise for static file serving
- **Database Optimization**: Efficient queries with select_related
- **Caching**: Redis caching for frequently accessed data
- **Lazy Loading**: Optimized image and content loading

## Future Enhancements

- **AI-Powered Optimization**: Advanced ML models for CV improvement
- **LinkedIn Integration**: Import profile data from LinkedIn
- **Real-time Notifications**: WebSocket-based job alerts
- **Mobile App**: React Native mobile application
- **Multi-language Support**: Internationalization support
- **Advanced Analytics**: Detailed performance metrics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is developed as part of an academic minor project and is intended for educational purposes.

## Support

For support and queries, contact the development team:
- Email: team@atsoptimizer.com
- GitHub Issues: Create an issue in the repository

---

**Made with ❤️ by Team ATS**