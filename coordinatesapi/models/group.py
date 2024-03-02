'''Wedding guest groups. This table provides a way
to split full guest list into smaller sections
for less complicated seating decisions'''
from django.db import models
from .wedding import Wedding

class Group(models.Model):
    '''Wedding groups.
    List views only accessible through the wedding_planner join table.
    Retrieve, update, and delete views all go through uuid.
    Read_only wedding_planners do not get uuid string
    from the read_only serializer'''
    uuid = models. UUIDField()
    name = models.CharField(max_length=50)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name="groups")

    def guests(self):
        '''returns all guests fom the group_guest table
        related to this group'''
        return [guest_group.guest for guest_group in self.guest_groups.all()]
