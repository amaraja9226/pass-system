from django import forms
from datetime import datetime

class PassApplicationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Student Name",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your full name'})
    )
    email = forms.EmailField(
    label="Student Email",
    widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
)

    department = forms.CharField(
        max_length=100,
        label="Department",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your department'})
    )
    class_name = forms.CharField(
        max_length=50,
        label="Class",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your class'})
    )
    village = forms.CharField(
        max_length=100,
        label="Village",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your village'})
    )
    reason = forms.CharField(
        label="Reason for requesting pass",
        required=True,
         widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Reason for requesting pass',
            'rows': 3
        })
    
    )
       
    pass_days = forms.IntegerField(
        label="Number of Days for Pass",
        min_value=1,
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter number of days'})
    )
    application_date = forms.DateField(
        label="Application Date",
        initial=datetime.today,
        widget=forms.DateInput(attrs={'class':'form-control', 'readonly':'readonly'})
    )
    application_time = forms.TimeField(
        label="Application Time",
        initial=datetime.now().strftime("%H:%M:%S"),
        widget=forms.TimeInput(attrs={'class':'form-control', 'readonly':'readonly'})
    )
