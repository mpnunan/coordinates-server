'''Brides and grooms'''
from django.db import models
from .wedding import Wedding

class Participant(models.Model):
    '''Brides and grooms.
    List views only accessible through the wedding_planner join table.
    Retrieve, update, and delete views all go through uuid.
    Read_only wedding_planners do not get uuid string
    from the read_only serializer'''
    uuid = models.UUIDField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='participants')
    
    @property
    def full_name(self):
        '''Returns full name of participant for use
        in serializers that don't requre more detail'''
        return f'{self.first_name} {self.last_name}'
    
    def guests(self):
        '''Returns all guests related to this participant'''  
        return [guest_participant.guest for guest_participant in self.guest_participants.all()]
            
