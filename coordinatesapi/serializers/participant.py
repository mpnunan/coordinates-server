from rest_framework import serializers
from coordinatesapi.models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'uuid', 'full_name')
