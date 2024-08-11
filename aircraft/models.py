from django.db import models
from airline.models import Airline
from datetime import datetime


class AircraftQuerySet(models.QuerySet):
    def delete(self):
        return super().update(isDeleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(isDeleted=False)

    def dead(self):
        return self.filter(isDeleted=True)

class AircraftManager(models.Manager):
    ## querylerde isDeleted == false olanlari getirsin
    def get_queryset(self):
        return AircraftQuerySet(self.model , using=self._db).alive()


class Aircraft(models.Model):
    manufacturer_serial_number = models.CharField(max_length=50,unique=True)
    type = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    number_of_engines = models.IntegerField()  
    operator_airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default=False)

    objects = AircraftManager()
    
    ## Because of "manufacturer_serial_number" attribute is unique
    ## If add a object with same name after delete will cause a error!
    ## So, add timestamp after delete
    def delete(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.manufacturer_serial_number = f"{self.manufacturer_serial_number}_deleted_{timestamp}"
        self.isDeleted = True
        self.save()

    def __str__(self):
        return f"{self.manufacturer_serial_number}"
       
