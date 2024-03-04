from rest_framework import serializers
from coordinatesapi.models import Wedding, WeddingPlanner, Guest, Group, ReceptionTable, Participant

class ReadOnlyParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'full_name')


class WeddingPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPlanner
        fields = ('planner', 'primary', 'read_only')
        depth = 1

class ReadOnlyWeddingSerializer(serializers.ModelSerializer):
    planners = WeddingPlannerSerializer(many=True, read_only=True)
    participants = ReadOnlyParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'participants', 'planners')
        
class ReadOnlyGroupGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    class Meta:
        model = Guest
        fields = ('id', 'full_name', 'table_number')

class ReadOnlyGroupSerializer(serializers.ModelSerializer):
    guests = ReadOnlyGroupGuestSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'guests')
        
class ReadOnlyGroupSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'uuid', 'name')

class ReadOnlyLimitedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class ReadOnlyGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = ReadOnlyLimitedGroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'full_name', 'table_number', 'group', 'seated')
        
class ReadOnlyTableGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'full_name')

class ReadOnlyReceptionTableSerializer(serializers.ModelSerializer):
    guests = ReadOnlyTableGuestSerializer(many=True, read_only=True)
    class Meta:
        model = ReceptionTable
        fields = ('id', 'number', 'capacity', 'guests', 'full')
    
class ReadOnlyGuestListSerializer(serializers.ModelSerializer):
    guests = ReadOnlyGuestSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'guests')
        
class ReadOnlyTableListSerializer(serializers.ModelSerializer):
    reception_tables = ReadOnlyReceptionTableSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'reception_tables')
        
class ReadOnlyGroupListSerializer(serializers.ModelSerializer):
    groups = ReadOnlyGroupSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'groups')

class ReadOnlyGuestSerializerShallow(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = ReadOnlyGroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'full_name', 'table_number', 'group')

class ReadOnlyCoupleSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = ReadOnlyGroupSerializerShallow(read_only=True)
    partner = ReadOnlyGuestSerializerShallow(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'group', 'partner')

class ReadOnlyNestedGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'full_name')

class ReadOnlySortedGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = ReadOnlyGroupSerializerShallow(read_only=True)
    partner = ReadOnlyNestedGuestSerializer(read_only=True)
    problem_pairing = ReadOnlyNestedGuestSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name', 'table_number', 'group', 'family', 'party', 'primary', 'seated', 'partner', 'problem_pairing')
