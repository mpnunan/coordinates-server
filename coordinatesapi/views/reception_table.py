from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import ReceptionTable, Wedding


class ReceptionTableView(ViewSet):

    def retrieve(self, request, pk):
        try:
            reception_table = ReceptionTable.objects.get(pk=pk)
            serializer = ReceptionTableSerializer(reception_table)
            return Response(serializer.data)
        except ReceptionTable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        reception_tables = ReceptionTable.objects.all()
        serializer = ReceptionTableSerializerShallow(reception_tables, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        reception_table = ReceptionTable.objects.create(
            wedding=wedding,
            nunmber=request.data["number"],
            capacity=request.data["capacity"]
        )
        serializer = ReceptionTableSerializerShallow(reception_table)
        return Response(serializer.data)
    
    def update(self, request, pk):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        reception_table = ReceptionTable.objects.get(pk=pk)
        reception_table.wedding=wedding
        reception_table.number=request.data["number"]
        reception_table.capacity=request.data["capacity"]
        reception_table.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        reception_table = ReceptionTable.objects.get(pk=pk)
        reception_table.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ReceptionTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionTable
        fields = ('id', 'wedding', 'number', 'capacity')
        depth = 2
        
class ReceptionTableSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = ReceptionTable
        fields = ('id', 'wedding', 'number', 'capacity')
