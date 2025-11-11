from django.db import models

VILLAGE_AMOUNT_MAPPING = {
    'Village A': 100,
    'Village B': 150,
    'Village C': 200,
    'Village D': 250,
    'Village E': 300,
}

class IssuePass(models.Model):
    pass_number = models.AutoField(primary_key=True)
    receipt_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(auto_now_add=True)

    # 👇 Signatures
    student_signature = models.FileField(upload_to="signatures/student/", null=True, blank=True)
    sub_admin_signature = models.FileField(upload_to="signatures/subadmin/", null=True, blank=True)
    admin_signature = models.FileField(upload_to="signatures/admin/", null=True, blank=True)

    # 👇 Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Sent', 'Sent')],
        default='Pending'
    )

    def __str__(self):
        return f"Pass #{self.pass_number} - {self.student_name}"

    @staticmethod
    def get_amount_for_village(village):
        return VILLAGE_AMOUNT_MAPPING.get(village, 100)
