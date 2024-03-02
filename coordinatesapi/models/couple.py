'''Join table for guests who are couples'''
from django.db import models
from .guest import Guest

class Couple(models.Model):
    '''Couple model is accessed through guest model,
    it has no direct views'''
    first_guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='couple_firsts')
    second_guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='couple_seconds')
