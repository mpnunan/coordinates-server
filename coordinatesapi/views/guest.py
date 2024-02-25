from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Guest, TableGuest, Wedding, ReceptionTable
from coordinatesapi.serializers import GroupSerializer


class GuestView(ViewSet):

    def retrieve(self, request, pk):
        try:
            guest = Guest.objects.get(pk=pk)
            
            guest.seated = len(TableGuest.objects.filter(
                guest_id=guest
            )) > 0
            
            serializer = GuestSerializer(guest)
            return Response(serializer.data)
        except Guest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        guests = Guest.objects.all()
        
        wedding = request.query_params.get('wedding', None)
        if wedding is not None:
            guests = guests.filter(wedding_id=wedding)
        else:
            guests = []
            
        for guest in guests:
            guest.seated = len(TableGuest.objects.filter(
                guest_id=guest
            )) > 0
        
        
        serializer = GuestSerializerShallow(guests, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        guest = Guest.objects.create(
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
            wedding=wedding,
        )
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def update(self, request, pk):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        guest = Guest.objects.get(pk=pk)
        guest.first_name=request.data["firstName"]
        guest.last_name=request.data["lastName"]
        guest.wedding=wedding
        guest.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        guest = Guest.objects.get(pk=pk)
        guest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GuestSerializerShallow(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'full_name', 'table_number', 'group', 'seated')
        
class GuestSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(default=None)
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'first_name', 'last_name', 'wedding_id', 'table_number', 'group', 'seated')
