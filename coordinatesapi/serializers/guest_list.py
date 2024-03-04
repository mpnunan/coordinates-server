from rest_framework import serializers
from coordinatesapi.models import Guest
from .group import GroupSerializerShallow

class NestedGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name')

class SortedGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializerShallow(read_only=True)
    partner = NestedGuestSerializer(read_only=True)
    problem_pairing = NestedGuestSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'group', 'family', 'party', 'primary', 'seated', 'partner', 'problem_pairing')
