from django.urls import path
from . import views

app_name = 'cv_optimizer'

urlpatterns = [
    path('upload/', views.CVUploadView.as_view(), name='upload'),
    path('analyze/<int:cv_id>/', views.CVAnalysisView.as_view(), name='analyze'),
    path('optimize/<int:cv_id>/', views.CVOptimizeView.as_view(), name='optimize'),
    path('download/<int:cv_id>/', views.DownloadOptimizedCV.as_view(), name='download'),
    path('delete/<int:cv_id>/', views.DeleteCVView.as_view(), name='delete'),
    path('history/', views.CVHistoryView.as_view(), name='history'),
]