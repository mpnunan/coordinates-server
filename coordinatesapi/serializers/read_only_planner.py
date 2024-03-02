from rest_framework import serializers
from coordinatesapi.models import Wedding, WeddingPlanner, Guest, Group, ReceptionTable

class WeddingPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPlanner
        fields = ('planner', 'primary', 'read_only')
        depth = 1

class ReadOnlyWeddingSerializer(serializers.ModelSerializer):
    planners = WeddingPlannerSerializer(many=True, read_only=True)
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planners')

class ReadOnlyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class ReadOnlyGuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = ReadOnlyGroupSerializer(read_only=True)
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
        depth = 1

        
class ReadOnlyGuestListSerializer(serializers.ModelSerializer):
    guests = ReadOnlyGuestSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'guests')
        depth = 1
        
class ReadOnlyTableListSerializer(serializers.ModelSerializer):
    reception_tables = ReadOnlyReceptionTableSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'reception_tables')
        depth = 2
        
class ReadOnlyGroupListSerializer(serializers.ModelSerializer):
    groups = ReadOnlyGroupSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'groups')
