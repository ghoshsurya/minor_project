@echo off
echo 🚀 ATS CV Optimizer - Quick Setup
echo ================================

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

echo 👑 Creating superuser...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@atsoptimizer.com', 'admin123')"

echo 📊 Collecting static files...
python manage.py collectstatic --noinput

echo ✅ Setup completed!
echo 🌐 Starting server...
echo 📊 Flowchart: http://127.0.0.1:8000/flowchart/
echo 🔐 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)
echo 🏠 Main: http://127.0.0.1:8000/

python manage.py runserver