from django.contrib import admin
from .models import RenewPass

@admin.register(RenewPass)
class RenewPassAdmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'original_receipt_id', 'name', 'photo','payment_status',  'student_class', 'department', 'village', 'month', 'amount', 'created_at')
    search_fields = ('receipt_id', 'original_receipt_id', 'name', 'student_class', 'department','payment_status')
    list_filter = ('department', 'month', 'created_at','payment_status')
