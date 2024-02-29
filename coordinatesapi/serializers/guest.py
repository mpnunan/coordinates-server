from rest_framework import serializers
from coordinatesapi.models import Guest
from .group import GroupSerializer

class GuestSerializerShallow(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'full_name', 'table_number', 'group', 'seated')
        
class GuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'first_name', 'last_name', 'wedding_id', 'table_number', 'group', 'seated')
