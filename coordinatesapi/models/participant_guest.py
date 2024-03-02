'''This model is a join table to show which side of the
wedding a guest is on. The family boolean equal to True
is the only instance of a wedding participant's family.
The party boolean equal to true is the only indicator
of a participant's wedding party. The primary boolean indicates
best man/woman or maid/man of honor'''
from django.db import models
from .guest import Guest
from .participant import Participant

class ParticipantGuest(models.Model):
    '''This model does not have much impact on CRUD
    and serves an informational role for a user
    to aid seating decision-making. This model is the ony
    join table that has direct views'''
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='participant_guests')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='guest_participants')
    family = models.BooleanField(null=True)
    party = models.BooleanField(null=True)
    primary = models.BooleanField(null=True)
