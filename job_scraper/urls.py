from django.urls import path
from . import views

app_name = 'job_scraper'

urlpatterns = [
    path('search/', views.JobSearchView.as_view(), name='search'),
    path('job/<int:job_id>/', views.JobDetailView.as_view(), name='detail'),
    path('alerts/', views.JobAlertsView.as_view(), name='alerts'),
    path('alerts/create/', views.CreateJobAlertView.as_view(), name='create_alert'),
    path('scrape/', views.ScrapeJobsView.as_view(), name='scrape'),
]