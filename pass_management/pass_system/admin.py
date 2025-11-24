from django.contrib import admin
from .models import IssuePass

@admin.register(IssuePass)
class IssuePassAdmin(admin.ModelAdmin):
    list_display = [
        'pass_number', 'receipt_id', 'student_name', 'student_class', 
        'department', 'village', 'amount', 'issue_date', 'month', 'student_uploaded_photo'
    ]
    list_filter = ['village', 'department', 'student_class', 'issue_date']
    search_fields = ['receipt_id', 'student_name', 'village']
    ordering = ['-issue_date']
    readonly_fields = ['pass_number', 'issue_date']  # keep only fields you don't want to edit
