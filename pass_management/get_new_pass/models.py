# models.py
from django.db import models

class PassApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    pass_days = models.CharField(max_length=50)
    application_date = models.DateField()
    application_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    receipt_id = models.CharField(max_length=100, blank=True, null=True)  # stores generated ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
