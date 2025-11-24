from django.db import models
from pass_system.models import IssuePass
import uuid  # for generating unique IDs


class RenewPass(models.Model):
    receipt_id = models.CharField(max_length=20, unique=True, blank=True)  # auto-generate
    original_receipt_id = models.CharField(max_length=20)  # purana receipt id
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    village = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    month = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='renew_photos/', blank=True, null=True)
    signature = models.ImageField(upload_to='renew_signatures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default="UNPAID")


    def save(self, *args, **kwargs):
        if not self.receipt_id:
            # generate a unique receipt ID (first 8 chars of UUID)
            self.receipt_id = str(uuid.uuid4()).replace('-', '')[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_id
