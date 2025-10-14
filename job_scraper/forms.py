from django import forms
from .models import UserJobAlert

class JobSearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search jobs, companies, or keywords...'
        })
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        })
    )
    job_type = forms.ChoiceField(
        choices=[
            ('', 'All Types'),
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
            ('remote', 'Remote')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    experience = forms.ChoiceField(
        choices=[
            ('', 'All Levels'),
            ('fresher', 'Fresher'),
            ('1-3', '1-3 Years'),
            ('3-5', '3-5 Years'),
            ('5+', '5+ Years')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class JobAlertForm(forms.ModelForm):
    class Meta:
        model = UserJobAlert
        fields = ['keywords', 'location', 'job_type', 'is_active']
        widgets = {
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python Developer, Data Scientist'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mumbai, Bangalore, Remote'
            }),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_type'].choices = [
            ('', 'All Types'),
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
            ('remote', 'Remote')
        ]
        self.fields['job_type'].required = False
        self.fields['location'].required = False
        self.fields['is_active'].initial = True