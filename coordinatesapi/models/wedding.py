from django.db import models
from .planner import Planner

class Wedding(models.Model):

    venue = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def guests(self):
        return [guest.self for guest in self.guests.all()]

    def reception_tables(self):
        return [reception_table.self for reception_table in self.reception_tables.all()]

    def planners(self):
        return [planner_wedding for planner_wedding in self.planner_weddings.all()]
