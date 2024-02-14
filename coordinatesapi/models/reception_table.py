from django.db import models
from .wedding import Wedding

class ReceptionTable(models.Model):
  
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)
    number = models.IntegerField()
    capacity = models.IntegerField()
    
    @property
    def full(self):
        return self.__full
    
    @full.setter
    def full(self, value):
        self.__full = value
