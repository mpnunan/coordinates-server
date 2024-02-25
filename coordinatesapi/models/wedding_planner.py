from django.db import models
from .wedding import Wedding
from .planner import Planner

class WeddingPlanner(models.Model):
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='planner_weddings')
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE, related_name='wedding_planners')
    primary = models.BooleanField(null=True)
    read_only = models.BooleanField(null=True)
