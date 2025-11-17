from django import forms
from .models import IssuePass
from get_new_pass.models import PassApplication

class IssuePassForm(forms.ModelForm):
    class Meta:
        model = IssuePass
        fields = [
            'receipt_id',
            'student_name',
            'student_class',
            'department',
            'village',
            'amount',
        ]


        widgets = {
            'receipt_id': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter Receipt ID', 'id': 'receipt_id'
            }),
            'student_name': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly', 'id': 'student_name'
            }),
            'student_class': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly', 'id': 'student_class'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly', 'id': 'department'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control', 'readonly': 'readonly', 'id': 'village'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 'readonly': 'readonly', 'id': 'amount'
            }),
        }

        

