from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    COUNTRIES = (
        ('PL', 'Poland'),
        ('UK', 'United Kingdom'),
        ('US', 'United States'),

    )
    country = models.CharField(choices=COUNTRIES, max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)


class UserProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    purchases_made = models.IntegerField(default=0)
    purchases_value = models.IntegerField(default=0)
    about = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
