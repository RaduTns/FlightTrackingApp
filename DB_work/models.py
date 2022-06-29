from django.db import models

# Create your models here.

class Flight(models.Model):
    callsign = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    altitude = models.CharField(max_length=100, null=True)
    on_ground = models.CharField(max_length=100, null=True)

