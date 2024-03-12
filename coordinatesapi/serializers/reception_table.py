from rest_framework import serializers
from coordinatesapi.models import Guest, ReceptionTable

class TableGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'uuid', 'full_name')

class ReceptionTableSerializer(serializers.ModelSerializer):
    guests = TableGuestSerializer(many=True, read_only=True)
    class Meta:
        model = ReceptionTable
        fields = ('id', 'uuid', 'number', 'capacity', 'guests', 'full', 'wedding_id')
        depth = 1

class ReceptionTableSerializerShallow(serializers.ModelSerializer):
    guests = TableGuestSerializer(many=True, read_only=True)
    class Meta:
        model = ReceptionTable
        fields = ('id', 'uuid', 'number', 'capacity', 'guests', 'full', 'wedding_id')
