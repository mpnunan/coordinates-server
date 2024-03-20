from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from coordinatesapi.models import Planner, Wedding, WeddingPlanner, Participant, TableGuest, Guest, ReceptionTable, Group, Couple, Problem
from coordinatesapi.serializers import WeddingSerializerShallow, WeddingUpdateSerializer, PlannerWeddingSerializer, GuestListSerializer, WeddingSerializer, TableListSerializer, ReadOnlyWeddingSerializer, ReadOnlyGuestListSerializer, ReadOnlyTableListSerializer, GroupListSerializer, ReadOnlyGroupListSerializer, CoupleSerializer, ParticipantSerializer, ReadOnlyParticipantSerializer, WeddingPlannerSerializer
from rest_framework.decorators import action
import uuid
from django.db.models import Q

class WeddingView(ViewSet):

    def retrieve(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
            if wedding.read_only is True:
                serializer = ReadOnlyWeddingSerializer(wedding.wedding)
            else:
                serializer = WeddingSerializer(wedding.wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            weddings = WeddingPlanner.objects.filter(planner=planner)
            serializer = PlannerWeddingSerializer(weddings, many=True)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def create(self, request):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.create(
            uuid=uuid.uuid4(),
            venue=request.data["venue"],
            name=request.data["weddingName"],
        )
        WeddingPlanner.objects.create(
            wedding=wedding,
            planner=planner,
            primary=True,
        )
        serializer = WeddingSerializerShallow(wedding)
        return Response(serializer.data)
    
    def update(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.get(uuid=pk)
        try:
            WeddingPlanner.objects.get(planner=planner, wedding=wedding)
            wedding.venue=request.data["venue"]
            wedding.name=request.data["weddingName"]
            wedding.save()
            serializer = WeddingUpdateSerializer(wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.get(uuid=pk)
        try:
            WeddingPlanner.objects.get(planner=planner, wedding=wedding)
            wedding.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['get'], detail=True)
    def guests(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
            wedding.guests = Guest.objects.filter(wedding=__wedding)
                
            for guest in wedding.guests:
                guest.seated = len(TableGuest.objects.filter(
                    guest_id=guest
                )) > 0
                try:
                    couple = Couple.objects.get(first_guest=guest)
                    guest.partner = couple.second_guest
                except Couple.DoesNotExist:
                    pass
                try:
                    couple = Couple.objects.get(second_guest=guest)
                    guest.partner = couple.first_guest
                except Couple.DoesNotExist:
                    pass
                try:
                    problem = Problem.objects.get(first_guest=guest)
                    guest.problem = problem.second_guest
                except Problem.DoesNotExist:
                    pass
                try:
                    problem = Problem.objects.get(second_guest=guest)
                    guest.problem = problem.first_guest
                except Problem.DoesNotExist:
                    pass
            
            if wedding.read_only is True:
                serializer = ReadOnlyGuestListSerializer(wedding)
            else:
                serializer = GuestListSerializer(wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['get'], detail=True)
    def reception_tables(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
            wedding.reception_tables = ReceptionTable.objects.filter(wedding=__wedding)
            for reception_table in wedding.reception_tables:
                reception_table.full = len(TableGuest.objects.filter(
                    reception_table_id=reception_table
                )) > reception_table.capacity
            if wedding.read_only is True:
                serializer = ReadOnlyTableListSerializer(wedding)
            else:
                serializer = TableListSerializer(wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True)
    def groups(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
            wedding.groups = Group.objects.filter(wedding=__wedding)
            if wedding.read_only is True:
                serializer = ReadOnlyGroupListSerializer(wedding)
            else:
                serializer = GroupListSerializer(wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['get'], detail=True)
    def participants(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
            participants = Participant.objects.filter(wedding=__wedding)
           
            if wedding.read_only is True:
                serializer = ReadOnlyParticipantSerializer(participants, many=True)
            else:
                serializer = ParticipantSerializer(participants, many=True)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['get'], detail=True)
    def planners(self, request, pk):
        __planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            planner = WeddingPlanner.objects.get(planner=__planner, wedding=__wedding)
            if planner is not None:
                planners = WeddingPlanner.objects.filter(wedding=__wedding).exclude(planner=__planner)
                serializer = WeddingPlannerSerializer(planners, many=True)
                return Response(serializer.data)
        except WeddingPlanner.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    @action(methods=['post'], detail=True)
    def add_planner(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding_planner = Planner.objects.get((Q(email=request.data["email"]) | Q(phone_number=request.data["phoneNumber"])))
        try:
            wedding = Wedding.objects.get(pk=pk)
            WeddingPlanner.objects.get(planner=planner, wedding=wedding, primary=True)
            WeddingPlanner.objects.create(
                wedding=wedding,
                planner=wedding_planner,
                primary=False,
                read_only=request.data["readOnly"]
                )
            return Response({'message': 'Planner Added'}, status=status.HTTP_201_CREATED)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['put'], detail=True)
    def update_planner(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding_planner = Planner.objects.get((Q(email=request.data["email"]) | Q(phone_number=request.data["phoneNumber"])))
        try:
            wedding = Wedding.objects.get(pk=pk)
            WeddingPlanner.objects.get(planner=planner, wedding=wedding, primary=True)
            wedding_planner.read_only=request.data["readOnly"]
            wedding_planner.save()
            return Response({'message': 'Planner Updated'}, status=status.HTTP_204_NO_CONTENT)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
    @action(methods=['put'], detail=True)
    def remove_planner(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding_planner = Planner.objects.get((Q(email=request.data["email"]) | Q(phone_number=request.data["phoneNumber"])))
        try:
            wedding = Wedding.objects.get(pk=pk)
            WeddingPlanner.objects.get(planner=planner, wedding=wedding, primary=True)
            wedding_planner.destroy()
            return Response({'message': 'Planner Removed'}, status=status.HTTP_204_NO_CONTENT)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
