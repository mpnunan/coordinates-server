from django.db import models
from .planner import Planner

class Wedding(models.Model):

    venue = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    
    def guests(self):
        return [guest.self for guest in self.guests.all()]

    @property
    def planner(self):
        return self.__planner
    
    @planner.setter
    def planner(self, value):
        self.__planner = value
