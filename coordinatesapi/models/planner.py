'''The planner model is the application
user model'''
from django.db import models

class Planner(models.Model):
    '''This model can be accessed directly,
    but also controls wedding views through the
    relationship between planners and weddings
    on the wedding_planner model'''
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()
    uid = models.CharField(max_length=50)
    
    @property
    def full_name(self):
        '''Returns full name for serializers
        that do not need more details'''
        return f'{self.first_name} {self.last_name}'
