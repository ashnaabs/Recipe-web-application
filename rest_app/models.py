from django.db import models
from datetime import timedelta     #to import time data
# Create your models here.

class recipes(models.Model):
    name=models.CharField(max_length=250)
    prep_time=models.DurationField(default=timedelta(minutes=120))
    DIFFICULTY_CHOICES=[
        (1,'Easy'),
        (2,'Medium'),
        (3,'Hard'),
    ]
    difficulty=models.IntegerField(choices=DIFFICULTY_CHOICES)
    vegetarian=models.BooleanField()
    Recipe_img=models.ImageField(blank=True)
    description=models.CharField(max_length=5000)