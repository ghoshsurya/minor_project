from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from .models import CVUpload
from .forms import CVUploadForm
from .utils import analyze_cv, optimize_cv
import json

class CVUploadView(LoginRequiredMixin, CreateView):
    model = CVUpload
    form_class = CVUploadForm
    template_name = 'cv_optimizer/upload.html'
    success_url = reverse_lazy('cv_optimizer:history')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'CV uploaded successfully! Analysis in progress...')
        return response

class CVAnalysisView(LoginRequiredMixin, DetailView):
    model = CVUpload
    template_name = 'cv_optimizer/analysis.html'
    context_object_name = 'cv_upload'
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cv_upload = self.get_object()
        
        if not cv_upload.analysis_report:
            # Perform analysis
            analysis = analyze_cv(cv_upload.original_cv.path, cv_upload.job_role)
            cv_upload.ats_score = analysis['score']
            cv_upload.analysis_report = analysis
            cv_upload.save()
        
        context['analysis'] = cv_upload.analysis_report
        return context

class CVOptimizeView(LoginRequiredMixin, DetailView):
    model = CVUpload
    template_name = 'cv_optimizer/optimize.html'
    context_object_name = 'cv_upload'
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        cv_upload = self.get_object()
        
        if not cv_upload.optimized_cv:
            # Generate optimization tips instead of actual file
            optimization_tips = optimize_cv(cv_upload.original_cv.path, cv_upload.analysis_report)
            # Just mark as optimized without saving file
            cv_upload.analysis_report['optimization_tips'] = optimization_tips
            cv_upload.save()
        
        messages.success(request, 'CV optimization tips generated successfully!')
        return redirect('cv_optimizer:analyze', cv_id=cv_upload.id)

class DownloadOptimizedCV(LoginRequiredMixin, DetailView):
    model = CVUpload
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        cv_upload = self.get_object()
        
        if cv_upload.optimized_cv:
            response = HttpResponse(cv_upload.optimized_cv.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="optimized_{cv_upload.original_cv.name}"'
            return response
        
        messages.error(request, 'Optimized CV not available.')
        return redirect('cv_optimizer:analyze', cv_id=cv_upload.id)

class CVHistoryView(LoginRequiredMixin, ListView):
    model = CVUpload
    template_name = 'cv_optimizer/history.html'
    context_object_name = 'cv_uploads'
    paginate_by = 10
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)

class DeleteCVView(LoginRequiredMixin, DeleteView):
    model = CVUpload
    pk_url_kwarg = 'cv_id'
    success_url = reverse_lazy('cv_optimizer:history')
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'CV analysis deleted successfully!')
        return super().delete(request, *args, **kwargs)