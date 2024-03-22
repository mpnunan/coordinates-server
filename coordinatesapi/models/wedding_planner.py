'''All CRUD originates with this model.
Planners can only access weddings if they
are joined on the wedding_planner table.
'''
from django.db import models
from .wedding import Wedding
from .planner import Planner

class WeddingPlanner(models.Model):
    '''If a wedding_planner has the read_only boolean
    equal to True, they will be prevented from
    any create functions related to the read_only wedding,
    and the wedding list view will
    not pass the necessary uuid string needed for
    update or delete on any tables realted to the
    read_only wedding. Primary is equal to true
    if a planner is the original creator of a wedding'''
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='planner_weddings')
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE, related_name='wedding_planners')
    primary = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)
