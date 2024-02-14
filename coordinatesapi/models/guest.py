from django.db import models

class Guest(models.Model):
  
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
    @property
    def seated(self):
        return self.__seated
    
    @seated.setter
    def seated(self, value):
        self.__seated = value
