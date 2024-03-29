'''Join table for guests seated seated at reception_tables'''
from django.db import models
from .reception_table import ReceptionTable
from .guest import Guest

class TableGuest(models.Model):
    '''This model is access through the guest model
    or reception_table model, it has no direct views'''
    reception_table = models.ForeignKey(ReceptionTable, on_delete=models.CASCADE, related_name='guest_tables')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='table_guests')
