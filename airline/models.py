from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class AirlineQuerySet(models.QuerySet):
    def delete(self):
        return super().update(isDeleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(isDeleted=False)

    def dead(self):
        return self.filter(isDeleted=True)

class AirlineManager(models.Manager):
    ## querylerde isDeleted == false olanlari getirsin
    def get_queryset(self):
        return AirlineQuerySet(self.model , using=self._db).alive()


# name is unique
class Airline(models.Model):
    name = models.CharField(max_length=50,unique=True)
    callsign = models.CharField(max_length=50)
    founded_year = models.IntegerField( validators=[
            MaxValueValidator(2024),
            MinValueValidator(1800)
        ])  
    base_airport = models.CharField(max_length=50)
    isDeleted = models.BooleanField(default=False)

    objects = AirlineManager()

    def delete(self):
        # Bounded Aircraft's isDeleted=True 
        for aircraft in self.aircraft_set.all():
            aircraft.delete()  

        ## Because of "name" attribute is unique
        ## If add a object with same name after delete will cause a error!
        ## So, add timestamp after delete
    
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.name = f"{self.name}_deleted_{timestamp}"
        self.isDeleted = True
        self.save()

    def __str__(self):
        return f"{self.name}"
       
