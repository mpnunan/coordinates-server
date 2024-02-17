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
