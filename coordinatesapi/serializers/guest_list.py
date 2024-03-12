from rest_framework import serializers
from coordinatesapi.models import Guest
from .group import GroupSerializerShallow

class NestedGuestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name')

class SortedGuestListSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializerShallow(read_only=True)
    partner = NestedGuestListSerializer(read_only=True)
    problem = NestedGuestListSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'participant', 'full_name', 'table_number', 'group', 'family', 'parent', 'party', 'primary', 'seated', 'partner', 'problem')
        depth = 1


class GuestsSortedSerializer(serializers.Serializer):
    guests = serializers.ListField()
    family = serializers.ListField()
    party = serializers.ListField()
    couples = serializers.ListField()
    problems = serializers.ListField()
    class Meta:
        fields = ('guests', 'family', 'party', 'couples', 'problems')
        
class GuestListSerializerShallow(serializers.ModelSerializer):
    group = GroupSerializerShallow(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'participant', 'full_name', 'group', 'family', 'parent', 'party', 'primary', 'partner', 'problem')
        depth = 1

class GuestsUnseatedSerializer(serializers.Serializer):
    guests = serializers.ListField()
    length = serializers.IntegerField()
    class Meta:
        fields = ('guests', 'length')
