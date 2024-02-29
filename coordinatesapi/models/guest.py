from django.db import models
from .wedding import Wedding

class Guest(models.Model):
  
    uuid = models.UUIDField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='guests')
    
    def table_number(self):
        for table_guest in self.table_guests.all():
            return table_guest.reception_table.number
    
    def group(self):
        for group_guest in self.group_guests.all():
            try:
                group = group_guest.group
            except group.DoesNotExist:
                group = 0
            return group
    
    @property
    def seated(self):
        return self.__seated
    
    @seated.setter
    def seated(self, value):
        self.__seated = value
        
    @property
    def single(self):
        return self.__single
    
    @single.setter
    def single(self, value):
        self.__single = value
        
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
