from django.db import models

# Create your models here.

class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField("Building Name", max_length=20)

    def __str__(self):
        return self.name

class Meter(models.Model):
    id = models.IntegerField(primary_key=True)
    building = models.ForeignKey('Building', on_delete=models.CASCADE, blank=True )
    fuel = models.CharField(max_length=30)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.fuel 

class HalfHourly(models.Model):
    consumption = models.FloatField(null=True, blank=True, default=None)
    meter = models.ForeignKey('Meter', on_delete=models.CASCADE, null=True, blank=True)
    reading_date_time = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.consumption)