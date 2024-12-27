from django.contrib.auth.models import User
from django.db import models
from userapp.models import Patient, Sex
from doctorapp.models import DoctorPatient, Doctor


# Create your models here.
class Insurance(models.Model):  # Fixed class inheritance syntax
    provider_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='gallery')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    maximum_coverage = models.IntegerField()
    policy_number = models.CharField(max_length=50)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return self.provider_name

class Bill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    injection_amount=models.IntegerField()
    scanning_amount=models.IntegerField()
    drugs_amount=models.IntegerField()
    surgery_amount=models.IntegerField()
    ward_procedures=models.IntegerField()
    doctor_fee=models.IntegerField()
    issue_date=models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,
        default='Pending')


    def __str__(self):
        return self.injection_amount

class Report(models.Model):
    doctor_name = models.CharField(max_length=100)
    scheduledtime = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    treatment= models.CharField(max_length=100)