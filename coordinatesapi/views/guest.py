from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Guest, TableGuest, Wedding
from coordinatesapi.serializers import GuestSerializer, GuestSerializerShallow
import uuid


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
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        guest = Guest.objects.create(
            uuid=uuid.uuid4(),
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
            wedding=wedding,
        )
        serializer = GuestSerializerShallow(guest)
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
