'''Weddings'''
from django.db import models

class Wedding(models.Model):
    '''The views for the wedding table can only be accessed
    through the wedding_planner join table.
    Read_only list serializers are used for wedding_planners
    with the read_only boolean set True'''
    uuid = models.UUIDField()
    venue = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def guests(self):
        '''Returns all guests related to this wedding'''
        return [guest.self for guest in self.guests.all()]

    def reception_tables(self):
        '''returns all receptoin_tables related to this wedding'''
        return [reception_table.self for reception_table in self.reception_tables.all()]

    def planners(self):
        '''returns all planners from wedding_planner join table related to this wedding'''
        return [planner_wedding for planner_wedding in self.planner_weddings.all()]

    def groups(self):
        '''returns all groups related to this wedding'''
        return [group.self for group in self.groups.all()]
