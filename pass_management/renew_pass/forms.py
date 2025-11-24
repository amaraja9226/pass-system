from django import forms
from .models import RenewPass

class RenewPassForm(forms.ModelForm):
    class Meta:
        model = RenewPass
        fields = [
            'original_receipt_id',  # purana receipt ID
            'name',
            'student_class',
            'department',
            'village',
            'amount',
            'month',
            'photo',
            'signature',
        ]

        widgets = {
            'old_receipt_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter old receipt ID',
                'id': 'receipt_id'
            }),
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'student_name'}),
            'student_class': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'student_class'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'department'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'village'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'amount'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'month'}),
            'student_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'student_signature': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
