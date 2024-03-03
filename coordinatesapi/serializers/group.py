from rest_framework import serializers
from coordinatesapi.models import Group, Guest

class GroupGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'seated')

class GroupSerializer(serializers.ModelSerializer):
    guests = GroupGuestSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'uuid', 'name', 'guests')

class GroupSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'uuid', 'name')
