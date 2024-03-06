from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from coordinatesapi.models import Group, Wedding
from coordinatesapi.serializers import GroupSerializer, ReadOnlyGroupSerializer
import uuid
from rest_framework.decorators import action


class GroupView(ViewSet):

    def retrieve(self, request, pk):
        try:
            group = Group.objects.get(uuid=pk)
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        group = Group.objects.create(
            uuid=uuid.uuid4(),
            name=request.data["name"],
            wedding=wedding,
        )
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    
    def update(self, request, pk):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        group = Group.objects.get(uuid=pk)
        group.name=request.data["name"]
        group.wedding=wedding
        group.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        group = Group.objects.get(uuid=pk)
        group.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['get'], detail=True)
    def read_only(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            serializer = ReadOnlyGroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
