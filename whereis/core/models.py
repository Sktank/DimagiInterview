from django.db import models

# Create your models here.

class Employee(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    numLocations = models.IntegerField()


class Location(models.Model):
    lng = models.FloatField()
    lat = models.FloatField()
    address = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee)
    time = models.DateTimeField()