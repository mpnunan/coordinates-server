from django.db import models

class Planner(models.Model):
  
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()
    uid = models.CharField(max_length=50)
