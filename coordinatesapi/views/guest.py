from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from coordinatesapi.models import Guest, TableGuest, Wedding, Participant, Planner, WeddingPlanner
from coordinatesapi.serializers import GuestCreatedSerializer, GuestSerializer, GuestSerializerShallow, ReadOnlyGuestSerializer
import uuid
from rest_framework.decorators import action


class GuestView(ViewSet):

    def retrieve(self, request, pk):
        try:
            guest = Guest.objects.get(uuid=pk)
            
            guest.seated = len(TableGuest.objects.filter(
                guest_id=guest
            )) > 0
            
            serializer = GuestSerializer(guest)
            return Response(serializer.data)
        except Guest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        wedding = Wedding.objects.get(pk=request.data["wedding"])
        participant = Participant.objects.get(uuid=request.data["participant"])
        __planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            planner = WeddingPlanner.objects.get(planner=__planner, wedding=wedding)
            if planner.read_only is True:
                pass
            else:
                guest = Guest.objects.create(
                uuid=uuid.uuid4(),
                first_name=request.data["firstName"],
                last_name=request.data["lastName"],
                wedding=wedding,
                participant = participant,
                family = request.data["family"],
                parent = request.data["parent"],
                party = request.data["party"],
                primary = request.data["primary"],
                )
                serializer = GuestCreatedSerializer(guest)
                return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    def update(self, request, pk):
        participant = Participant.objects.get(uuid=request.data["participant"])
        guest = Guest.objects.get(uuid=pk)
        guest.first_name=request.data["firstName"]
        guest.last_name=request.data["lastName"]
        guest.participant = participant
        guest.family = request.data["family"]
        guest.parent = request.data["parent"]
        guest.party = request.data["party"]
        guest.primary = request.data["primary"]
        guest.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        guest = Guest.objects.get(uuid=pk)
        guest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['get'], detail=True)
    def read_only(self, request, pk):
        try:
            guest = Guest.objects.get(pk=pk)
            
            guest.seated = len(TableGuest.objects.filter(
                guest_id=guest
            )) > 0
            
            serializer = ReadOnlyGuestSerializer(guest)
            return Response(serializer.data)
        except Guest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
