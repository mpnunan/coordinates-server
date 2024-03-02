from rest_framework import serializers
from coordinatesapi.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'uuid', 'name')
