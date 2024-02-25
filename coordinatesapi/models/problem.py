from django.db import models
from .guest import Guest

class Problem(models.Model):
    first_guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='first_problems')
    second_guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='second_problems')
    notes = models.CharField(max_length=200)
