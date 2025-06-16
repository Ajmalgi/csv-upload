from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)