'''Wedding reception tables'''
from django.db import models
from .wedding import Wedding

class ReceptionTable(models.Model):
    '''Wedding reception tables.
    List views only accessible through the wedding_planner join table.
    Retrieve, update, and delete views all go through uuid.
    Read_only wedding_planners do not get uuid string
    from the read_only serializer'''
    uuid = models.UUIDField()
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='reception_tables')
    number = models.IntegerField()
    capacity = models.IntegerField()

    def guests(self):
        '''returns all guestsn seated at this table'''
        return [guest_table.guest for guest_table in self.guest_tables.all()]  

    @property
    def full(self):
        '''if the number of guests seated at this table 
        is equal to the table capacity, full is set True'''
        return self.__full

    @full.setter
    def full(self, value):
        self.__full = value
