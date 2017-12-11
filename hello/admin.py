from django.contrib import admin
from django.forms.widgets import TextInput

#from django_google_maps.widgets import GoogleMapsAddressWidget
#from django_google_maps.fields import AddressField, GeoLocationField

from hello import models

#class RentalAdmin(admin.ModelAdmin):
#    formfield_overrides = {
#        AddressField: {'widget': GoogleMapsAddressWidget},
#        GeoLocationField: {'widget': TextInput(attrs={'readonly': 'readonly'})},
#    }
#
#admin.site.register(models.Rental, RentalAdmin)
#
#from .models import Foodlist
#
#admin.site.register(Foodlist)

# Register your models here.


#python manage.py makemigrations
#python manage.py migrate