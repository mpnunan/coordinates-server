from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Guest, TableGuest


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
        
        for guest in guests:
            guest.seated = len(TableGuest.objects.filter(
                guest_id=guest
            )) > 0
        
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        guest = Guest.objects.create(
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
        )
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def update(self, request, pk):
        guest = Guest.objects.get(pk=pk)
        guest.first_name=request.data["firstName"]
        guest.last_name=request.data["lastName"]
        guest.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        guest = Guest.objects.get(pk=pk)
        guest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'first_name', 'last_name', 'seated')
