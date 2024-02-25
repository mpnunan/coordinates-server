from django.db import models
from .group import Group
from .guest import Guest

class GroupGuest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='guest_groups')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='group_guests')
