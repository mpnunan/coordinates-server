from django.db import models
from .planner import Planner

class Wedding(models.Model):

    venue = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
