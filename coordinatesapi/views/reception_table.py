from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from coordinatesapi.models import ReceptionTable, Wedding, TableGuest, Guest, Planner, WeddingPlanner
from coordinatesapi.serializers import ReceptionTableSerializer, ReceptionTableSerializerShallow, ReadOnlyReceptionTableSerializer
import uuid


class ReceptionTableView(ViewSet):

    def retrieve(self, request, pk):
        try:
            reception_table = ReceptionTable.objects.get(uuid=pk)
            
            reception_table.full = len(TableGuest.objects.filter(
                reception_table_id=reception_table
            )) > reception_table.capacity
            
            serializer = ReceptionTableSerializer(reception_table)
            return Response(serializer.data)
        except ReceptionTable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        __planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            planner = WeddingPlanner.objects.get(planner=__planner, wedding=wedding)
            if planner.read_only is True:
                pass
            else:
                __number = ReceptionTable.objects.filter(wedding=wedding)
                number = len(__number) + 1
                reception_table = ReceptionTable.objects.create(
                    uuid=uuid.uuid4(),
                    wedding=wedding,
                    number=number,
                    capacity=request.data["capacity"]
                )
                serializer = ReceptionTableSerializerShallow(reception_table)
                return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    def update(self, request, pk):
        reception_table = ReceptionTable.objects.get(uuid=pk)
        reception_table.capacity=request.data["capacity"]
        reception_table.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        reception_table = ReceptionTable.objects.get(uuid=pk)
        __reception_tables = ReceptionTable.objects.filter(wedding=reception_table.wedding)
        for __reception_table in __reception_tables:
            if __reception_table.number > reception_table.number:
                __reception_table.number = __reception_table.number - 1
                __reception_table.save()
        reception_table.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    @action(methods=['post'], detail=True)
    def add_guest(self, request, pk):
        reception_table=ReceptionTable.objects.get(uuid=pk)
        guest=Guest.objects.get(uuid=request.data["guest"])
        TableGuest.objects.create(
          reception_table=reception_table,
          guest=guest,
        )
        return Response({'message': 'Guest added'}, status=status.HTTP_201_CREATED)
      
    @action(methods=['put'], detail=True)
    def remove_guest(self, request, pk):
        reception_table=ReceptionTable.objects.get(uuid=pk)
        guest=Guest.objects.get(uuid=request.data["guest"])
        table_guest = TableGuest.objects.filter(
          reception_table=reception_table,
          guest=guest,
        )
        table_guest.delete()
        return Response({'message': 'Guest Removed'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True)
    def read_only(self, request, pk):
        try:
            reception_table = ReceptionTable.objects.get(pk=pk)
            
            reception_table.full = len(TableGuest.objects.filter(
                reception_table_id=reception_table
            )) > reception_table.capacity
            
            serializer = ReadOnlyReceptionTableSerializer(reception_table)
            return Response(serializer.data)
        except ReceptionTable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
