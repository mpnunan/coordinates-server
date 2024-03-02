from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from coordinatesapi.models import ReceptionTable, Wedding, TableGuest, Guest
from coordinatesapi.serializers import ReceptionTableSerializer, ReceptionTableSerializerShallow
import uuid


class ReceptionTableView(ViewSet):

    def retrieve(self, request, string):
        try:
            reception_table = ReceptionTable.objects.get(uuid=string)
            
            reception_table.full = len(TableGuest.objects.filter(
                reception_table_id=reception_table
            )) > reception_table.capacity
            
            serializer = ReceptionTableSerializer(reception_table)
            return Response(serializer.data)
        except ReceptionTable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        reception_table = ReceptionTable.objects.create(
            uuid=uuid.uuid4(),
            wedding=wedding,
            number=request.data["number"],
            capacity=request.data["capacity"]
        )
        serializer = ReceptionTableSerializerShallow(reception_table)
        return Response(serializer.data)
    
    def update(self, request, string):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        reception_table = ReceptionTable.objects.get(uuid=string)
        reception_table.wedding=wedding
        reception_table.number=request.data["number"]
        reception_table.capacity=request.data["capacity"]
        reception_table.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, string):
        reception_table = ReceptionTable.objects.get(uuid=string)
        reception_table.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    @action(methods=['post'], detail=True)
    def add_guest(self, request, string):
        reception_table=ReceptionTable.objects.get(uuid=string)
        guest=Guest.objects.get(uuid=request.data["guest"])
        table_guest = TableGuest.objects.create(
          reception_table=reception_table,
          guest=guest,
        )
        return Response({'message': 'Guest added'}, status=status.HTTP_201_CREATED)
      
    @action(methods=['put'], detail=True)
    def remove_guest(self, request, string):
        reception_table=ReceptionTable.objects.get(uuid=string)
        guest=Guest.objects.get(uuid=request.data["guest"])
        table_guest = TableGuest.objects.filter(
          reception_table=reception_table,
          guest=guest,
        )
        table_guest.delete()
        return Response({'message': 'Guest Removed'}, status=status.HTTP_204_NO_CONTENT)
