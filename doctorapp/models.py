from django.db import models
from django.forms import ImageField

from userapp.models import Patient  # Ensure this is correct


class Name(models.Model):
    Doctorname = models.CharField(max_length=100)  # Adjust max_length as needed

    def __str__(self):
        return self.Doctorname  # Return the name field correctly


class Doctor(models.Model):
    doctor_name= models.ForeignKey(  # Renamed the field for clarity
        Name, on_delete=models.CASCADE, related_name="doctors"
    )
    schedule = models.TextField()
    specialization=models.CharField(max_length=20)
    Image=models.ImageField(upload_to='photos')

    def __str__(self):
            return self.doctor_name.Doctorname


class DoctorPatient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_visits')
    age = models.IntegerField(default=0)
    prescription = models.TextField()
    diagnosis = models.TextField()

    def __str__(self):
        return self.patient

