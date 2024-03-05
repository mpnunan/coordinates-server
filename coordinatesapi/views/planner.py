from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from coordinatesapi.models import Planner
from coordinatesapi.serializers import PlannerDetailSerializer

class PlannerView(ViewSet):
    
    def retrieve(self, request, pk):
        uid = request.META['HTTP_AUTHORIZATION']
        response = ''
        try:
            planner = Planner.objects.get(uid=uid)
            try:
                planner = Planner.objects.get(pk=pk)
                serializer = PlannerDetailSerializer(planner)
                response = Response(serializer.data)
            except Planner.DoesNotExist as ex:
                response =  Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Planner.DoesNotExist:
            response = Response({'message': 'Not Authorized'}, status=status.HTTP_404_NOT_FOUND)
        return response
    def update(self, request, pk):
        uid = request.META['HTTP_AUTHORIZATION']
        planner = Planner.objects.get(pk=pk)
        if uid == planner.uid:
            planner.first_name = request.data["firstName"]
            planner.last_name = request.data["lastName"]
            planner.email = request.data["email"]
            planner.phone_number = request.data["phoneNumber"]
            planner.save()
        else:
            pass
        return Response(None, status=status.HTTP_204_NO_CONTENT)
