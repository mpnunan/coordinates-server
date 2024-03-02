'''Join table for guests in groups'''
from django.db import models
from .group import Group
from .guest import Guest

class GroupGuest(models.Model):
    '''This model accessed through guest model or
    group model, it has no direct views'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='guest_groups')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='group_guests')
