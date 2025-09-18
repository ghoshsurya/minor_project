from django import forms
from .models import CVUpload

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CVUpload
        fields = ['original_cv', 'job_role']
        widgets = {
            'original_cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'id': 'cv-file'
            }),
            'job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Developer, Data Scientist, Marketing Manager'
            })
        }
    
    def clean_original_cv(self):
        cv_file = self.cleaned_data.get('original_cv')
        if cv_file:
            if cv_file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('File size must be less than 5MB.')
            
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = cv_file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError('Only PDF, DOC, and DOCX files are allowed.')
        
        return cv_file