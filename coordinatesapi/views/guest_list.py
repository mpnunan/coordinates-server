from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from coordinatesapi.models import Planner, Wedding, WeddingPlanner, Participant, ParticipantGuest, Couple, Problem, TableGuest
from coordinatesapi.serializers import SortedGuestSerializer, ReadOnlySortedGuestSerializer

class GuestListView(ViewSet):
    def retrieve(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            participant = Participant.objects.get(uuid=pk)
            __participant = ParticipantGuest.objects.filter(participant=participant)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=participant.wedding)
            for guest in participant.guests:
                guest.family = __participant.family
                guest.party = __participant.party
                guest.primary = __participant.primary
                guest.seated = len(TableGuest.objects.filter(
                    guest_id=guest
                )) > 0
                try:
                    couple = Couple.objects.get(first_guest=guest)
                    guest.partner = couple.second_guest
                except Couple.DoesNotExist:
                    pass
                try:
                    problem = Problem.objects.get(first_guest=guest)
                    guest.problem_pairing = problem
                except Problem.DoesNotExist:
                    pass
                
            if wedding.read_only is True:
                serializer = ReadOnlySortedGuestSerializer(participant.guests, many=True)
            else:
                serializer = SortedGuestSerializer(participant.guests, many=True)
            return Response(serializer.data)
        
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
