from django.db import models
from .guest import Guest
from .participant import Participant

class ParticipantGuest(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    family = models.BooleanField(null=True)
    party = models.BooleanField(null=True)
    primary = models.BooleanField(null=True)
