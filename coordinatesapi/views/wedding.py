from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Planner, Wedding


class WeddingView(ViewSet):

    def retrieve(self, request, pk):
        uid = request.META['HTTP_AUTHORIZATION']
        try:
            planner = Planner.objects.get(uid=uid)
            try:
                wedding = Wedding.objects.get(pk=pk)
                if wedding.planner == planner:
                    serializer = WeddingSerializer(wedding)
                    response = Response(serializer.data)
                else:
                    response =  Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            except Wedding.DoesNotExist as ex:
                response =  Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Planner.DoesNotExist:
            response = Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return response
    
    def list(self, request):
        weddings = Wedding.objects.all()
        uid = request.META['HTTP_AUTHORIZATION']
        try:
            planner = Planner.objects.get(uid=uid)
            weddings = Wedding.objects.filter(planner_id=planner)
            serializer = WeddingSerializerShallow(weddings, many=True)
            return Response(serializer.data)
        except Planner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def create(self, request):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.create(
            venue=request.data["venue"],
            name=request.data["name"],
            planner=planner
        )
        serializer = WeddingSerializerShallow(wedding)
        return Response(serializer.data)
    
    def update(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.get(pk=pk)
        wedding.venue=request.data["venue"]
        wedding.name=request.data["name"]
        wedding.planner=planner
        wedding.save()
        serializer = UpdateSerializer(wedding)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        uid=request.META['HTTP_AUTHORIZATION']
        try:
            planner = Planner.objects.get(uid=uid)
            wedding = Wedding.objects.filter(pk=pk, planner_id=planner)
            wedding.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Planner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planner')
        depth = 1
        
class WeddingSerializerShallow(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'venue', 'name', 'planner')
        
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ('id', 'name')
