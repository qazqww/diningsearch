from django.db import models
from django_google_maps.fields import AddressField, GeoLocationField

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
    
class Rental(models.Model):
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(blank=True)

    def __str__(self):
        return self.address
    
class Foodlist(models.Model):
    fname = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.fname