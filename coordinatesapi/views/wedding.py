from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Planner, Wedding


class WeddingView(ViewSet):

    def retrieve(self, request, pk):
        try:
            wedding = Wedding.objects.get(pk=pk)
            serializer = WeddingSerializer(wedding)
            return Response(serializer.data)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        weddings = Wedding.objects.all()
        serializer = WeddingSerializerShallow(weddings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        planner = Planner.objects.get(uid=request.data["planner"])
        wedding = Wedding.objects.create(
            venue=request.data["name"],
            name=request.data["email"],
            planner=planner
        )
        serializer = WeddingSerializerShallow(wedding)
        return Response(serializer.data)
    
    def update(self, request, pk):
        planner = Planner.objects.get(uid=request.data["planner"])
        wedding = Wedding.objects.get(pk=pk)
        wedding.venue=request.data["venue"]
        wedding.name=request.data["name"]
        wedding.planner=planner
        wedding.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        wedding = Wedding.objects.get(pk=pk)
        wedding.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planner')
        depth = 1
        
class WeddingSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planner')
