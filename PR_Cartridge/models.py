from django.db import models
class CartridgeRequest(models.Model):
    sl_no = models.AutoField(primary_key=True)   # new primary key field
    printer_no = models.CharField(max_length=200)
    employee_no = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    USAGE_CHOICES = [
        ('Self', 'Self'),
        ('Common Employee', 'Common Employee'),
    ]
    usage_status = models.CharField(
        max_length=100,
        choices=USAGE_CHOICES,
    )
    hod_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        default="Pending",  # <-- this line does the magic!
        blank=True,
        null=True,
    )
    hod_id = models.CharField(max_length=100, blank=True, null=True)
    request_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'cartridge_request'
    def __str__(self):
        return f"{self.employee_no} - {self.employee_name}"
class Employee(models.Model):
    emp_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=128)
    emp_name = models.CharField(max_length=100)
    emp_email= models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    class Meta:
        db_table = 'employee'
    def __str__(self):
        return f"{self.emp_id} - {self.emp_name}"
class MISAsset(models.Model):
    printer_no = models.CharField(max_length=100,primary_key=True)
    emp_no = models.CharField(max_length=50)
    emp_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    USAGE_CHOICES = [
        ('Self', 'Self'),
        ('Common Employee', 'Common Employee'),
    ]
    usage_status = models.CharField(max_length=100,choices=USAGE_CHOICES,)
    class Meta:
        db_table = 'MISAsset'
    def __str__(self):
        return f"{self.printer_no} - {self.emp_name}"