'''Wedding guests'''
from django.db import models
from .wedding import Wedding

class Guest(models.Model):
    '''Wedding guests.
    List views only accessible through the wedding_planner join table.
    Retrieve, update, and delete views all go through uuid.
    Read_only wedding_planners do not get uuid string
    from the read_only serializer'''

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
        '''If guest is present on table_guest
        join table, seated is set True'''
        return self.__seated

    @seated.setter
    def seated(self, value):
        self.__seated = value

    @property
    def single(self):
        '''If guest is not present on the couples table,
        single is set True'''
        return self.__single

    @single.setter
    def single(self, value):
        self.__single = value

    @property
    def full_name(self):
        '''Returns full name of guest for use
        in serializers that don't requre more detail'''
        return f'{self.first_name} {self.last_name}'
