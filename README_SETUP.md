# 🚀 ATS CV Optimizer - Quick Setup Guide

## Single Command Setup

### For Windows:
```bash
python start.py
```
or
```bash
setup.bat
```

### For Linux/Mac:
```bash
python start.py
```
or
```bash
chmod +x setup.sh
./setup.sh
```

## What the setup does:
1. ✅ Installs all Python dependencies
2. ✅ Sets up database with migrations
3. ✅ Creates admin user (admin/admin123)
4. ✅ Collects static files
5. ✅ Starts development server

## Access Points:
- 🏠 **Main Application**: http://127.0.0.1:8000/
- 👑 **Admin Panel**: http://127.0.0.1:8000/admin/ (admin/admin123)
- 📊 **Project Structure**: http://127.0.0.1:8000/flowchart/

## Project Architecture:

### Backend (Server-Side)
```
📁 Server/
├── ats_optimizer/     # Django project settings
├── accounts/          # User authentication
├── cv_optimizer/      # AI CV analysis
├── job_scraper/       # Job search & scraping
└── core/             # Core functionality
```

### Frontend (Client-Side)
```
📁 Client/
├── templates/        # HTML templates
├── static/          # CSS, JS, Images
└── media/           # User uploads
```

### Key Features:
- 🤖 **AI-Powered CV Analysis** using Google Gemini
- 🔍 **Real-time Job Search** from multiple portals
- 📄 **PDF Generation** with professional formatting
- 📝 **LaTeX Editor** for advanced CV creation
- 🎨 **Responsive Design** with Tailwind CSS
- 🌙 **Dark/Light Theme** toggle

## File Structure Overview:
```
MINOR PROJECT/
├── 🚀 start.py              # Single command startup
├── ⚙️ manage.py             # Django management
├── 📄 requirements.txt      # Dependencies
├── 🔧 .env                  # Environment variables
├── 🗄️ db.sqlite3           # Database
├── 📁 Backend Apps/         # Server-side logic
├── 📁 templates/            # Frontend templates
├── 📁 static/               # Static assets
└── 📁 media/                # User uploads
```

## Technology Stack:
- **Backend**: Django 4.2.7, Python 3.8+
- **AI/ML**: Google Gemini, NLTK, PyPDF2
- **Frontend**: Tailwind CSS, JavaScript ES6+
- **Database**: SQLite (PostgreSQL ready)
- **PDF**: ReportLab, LaTeX
- **Deployment**: Whitenoise, Gunicorn ready

## Development Commands:
```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Environment Variables (.env):
```
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///db.sqlite3
```

## Support:
For issues or questions, check the flowchart page at `/flowchart/` for detailed project structure and data flow diagrams.