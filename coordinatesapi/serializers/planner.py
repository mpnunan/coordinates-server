from rest_framework import serializers
from coordinatesapi.models import Planner, WeddingPlanner

class PlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planner
        fields = ('full_name', 'email', 'phone_number')

class WeddingPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPlanner
        fields = ('planner', 'primary', 'read_only')
        depth = 1

class PlannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planner
        fields = ('first_name', 'last_name', 'email', 'phone_number')
