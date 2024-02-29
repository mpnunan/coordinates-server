from django.db import models
from .wedding import Wedding

class ReceptionTable(models.Model):
  
    uuid = models.UUIDField()
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='reception_tables')
    number = models.IntegerField()
    capacity = models.IntegerField()
    
    def guests(self):
        return [guest_table.guest for guest_table in self.guest_tables.all()]  
    
    @property
    def full(self):
        return self.__full
    
    @full.setter
    def full(self, value):
        self.__full = value

    