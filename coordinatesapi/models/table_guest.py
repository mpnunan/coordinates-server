from django.db import models
from .reception_table import ReceptionTable
from .guest import Guest

class TableGuest(models.Model):
    
    reception_table = models.ForeignKey(ReceptionTable, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
