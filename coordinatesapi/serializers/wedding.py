from rest_framework import serializers
from coordinatesapi.models import Wedding, WeddingPlanner, Guest
from .guest import GuestSerializerShallow

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name')
  
class WeddingSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planner')
        
class WeddingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'name')
        
class PlannerWeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPlanner
        fields = ('wedding', 'primary', 'read_only')
        depth = 1
        
class PlannerWeddingGuestsSerializer(serializers.ModelSerializer):
    guests = GuestSerializerShallow(many=True, read_only=True)
    class Meta:
        model = WeddingPlanner
        fields = ('wedding', 'guests')
        depth = 1
