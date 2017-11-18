from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Foodlist(models.Model):
    fname = models.CharField(max_length=20)
    price = models.IntegerField(default=0)