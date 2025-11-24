from django.contrib import admin
from .models import PassApplication

@admin.register(PassApplication)
class PassApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'class_name', 'village', 'student_signature','pass_days', 'status', 'application_date', 'application_time', 'receipt_id', 'created_at','month')
    list_filter = ('status', 'department', 'village', 'application_date',)
   
