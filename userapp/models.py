from django.db import models
from django.apps import apps
from django.contrib.auth.models import User


class Sex(models.Model):
    sex = models.CharField(max_length=10)

    def __str__(self):
        return self.sex


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token_number = models.IntegerField(default=0)
    username = models.CharField(max_length=50, blank=True, default="")
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE, null=True, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=200, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    Image = models.ImageField(upload_to='book_media')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    Reason = models.TextField(max_length=200)

    def __str__(self):
        return self.name

