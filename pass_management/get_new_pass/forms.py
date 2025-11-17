from django import forms
from .models import PassApplication
from datetime import datetime

class PassApplicationForm(forms.ModelForm):
    class Meta:
        model = PassApplication
        fields = [
            'name', 'email', 'department', 'class_name', 'village',
            'reason', 'pass_days', 'application_date', 'application_time',
            'student_signature'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email'
            }),
            'department': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your department'
            }),
            'class_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your class'
            }),
            'village': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your village'
            }),
            'reason': forms.Textarea(attrs={
                'class':'form-control',
                'rows': 3,
                'placeholder':'Reason for requesting pass'
            }),
            'pass_days': forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter number of days'
            }),
            'application_date': forms.DateInput(attrs={
                'class':'form-control',
                'readonly':'readonly'
            }, format='%Y-%m-%d'),
            'application_time': forms.TimeInput(attrs={
                'class':'form-control',
                'readonly':'readonly'
            }, format='%H:%M:%S'),
            'student_signature': forms.ClearableFileInput(attrs={
                'class':'form-control'
            }),
        }

    # Set default values for date and time
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['application_date'].initial = datetime.today().date()
        self.fields['application_time'].initial = datetime.now().strftime("%H:%M:%S")
