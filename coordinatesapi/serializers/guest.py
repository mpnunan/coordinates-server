from rest_framework import serializers
from coordinatesapi.models import Guest
from .group import GroupSerializer, GroupSerializerShallow

class GuestSerializerShallow(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'group', 'seated')
        
class GuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'first_name', 'last_name', 'wedding_id', 'table_number', 'group', 'seated')

class CoupleSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializerShallow(read_only=True)
    partner = GuestSerializerShallow(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'group', 'partner')
