from django.db import models
from get_new_pass.models import PassApplication

class IssuePass(models.Model):
    pass_number = models.AutoField(primary_key=True)
    receipt_id = models.CharField(max_length=50,)
    student_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)  # optional
    student_class = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    pass_days = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    application_date = models.DateField(null=True, blank=True)
    application_time = models.TimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(auto_now_add=True)
    student_signature = models.FileField(upload_to='signatures/student/', null=True, blank=True)
    admin_signature = models.FileField(upload_to='signatures/admin/', null=True, blank=True)
    sub_admin_signature = models.FileField(upload_to='signatures/subadmin/', null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Sent', 'Sent')], default='Pending')
    month = models.CharField(max_length=20, null=True, blank=True)
    # Existing fields ke niche
    student_uploaded_photo = models.FileField(
    upload_to='student_photos/', null=True, blank=True
    )


    def __str__(self):
        return f"Pass #{self.pass_number} - {self.student_name}"

    @staticmethod
    def get_amount_for_village(village):
        return {'Village A': 100, 'Village B': 150}.get(village, 100)
