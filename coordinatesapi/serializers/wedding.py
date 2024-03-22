from rest_framework import serializers
from coordinatesapi.models import Wedding, WeddingPlanner
from .planner import WeddingPlannerSerializer
from .reception_table import ReceptionTableSerializer
from .group import GroupSerializer
from .participant import ParticipantSerializer
from .guest_list import SortedGuestListSerializer

class WeddingSerializer(serializers.ModelSerializer):
    planners = WeddingPlannerSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Wedding
        fields = ('id', 'uuid', 'venue', 'name', 'participants', 'planners')

class WeddingSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'uuid', 'venue', 'name')
        
class WeddingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'name')
        
class PlannerWeddingSerializer(serializers.ModelSerializer):
    wedding = WeddingSerializerShallow(read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding', 'planner_id', 'primary', 'read_only')
        depth = 1
        
class GuestListSerializer(serializers.ModelSerializer):
    guests = SortedGuestListSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'guests')
        
class TableListSerializer(serializers.ModelSerializer):
    reception_tables = ReceptionTableSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'reception_tables')

class GroupListSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'groups')

class SortedWeddingSerializer(serializers.Serializer):
    primary = serializers.ListField()
    read_only = serializers.ListField()
    shared = serializers.ListField()
    class Meta:
        fields = ('primary', 'read_only', 'shared')
