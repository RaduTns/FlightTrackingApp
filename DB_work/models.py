from django.db import models

# Create your models here.

class Flight(models.Model):
    callsign = models.CharField(max_length=100, primary_key=True)
    longitude = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    altitude = models.CharField(max_length=100, null=True)
    on_ground = models.CharField(max_length=100, null=True)
    origin = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)


class OriginAirports(models.Model):
    airport = models.CharField(max_length=100, primary_key=True)
    number_of_tracked_flights = models.IntegerField(null=False)

class DestinationAirports(models.Model):
    airport = models.CharField(max_length=100, primary_key=True)
    number_of_tracked_flights = models.IntegerField(null=False)