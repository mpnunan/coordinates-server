from rest_framework import serializers
from coordinatesapi.models import Wedding, WeddingPlanner
from .guest import GuestSerializerShallow
from .planner import WeddingPlannerSerializer
from .reception_table import ReceptionTableSerializer

class WeddingSerializer(serializers.ModelSerializer):
    planners = WeddingPlannerSerializer(many=True, read_only=True)
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planners')

class WeddingSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name')
        
class WeddingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'name')
        
class PlannerWeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPlanner
        fields = ('wedding', 'planner_id')
        depth = 1
        
class GuestListSerializer(serializers.ModelSerializer):
    guests = GuestSerializerShallow(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'guests')
        depth = 1
        
class TableListSerializer(serializers.ModelSerializer):
    reception_tables = ReceptionTableSerializer(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding_id' ,'reception_tables')
        depth = 2
