from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from coordinatesapi.models import Planner, Wedding, WeddingPlanner, TableGuest, Guest, ReceptionTable
from coordinatesapi.serializers import WeddingSerializerShallow, WeddingUpdateSerializer, PlannerWeddingSerializer, GuestListSerializer, WeddingSerializer, TableListSerializer
from rest_framework.decorators import action


class WeddingView(ViewSet):

    def retrieve(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            try:
                wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
                serializer = WeddingSerializer(wedding.wedding)
                return Response(serializer.data)
            except WeddingPlanner.DoesNotExist:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        try:
            planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
            weddings = WeddingPlanner.objects.filter(planner=planner)
            serializer = PlannerWeddingSerializer(weddings, many=True)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def create(self, request):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.create(
            venue=request.data["venue"],
            name=request.data["name"],
        )
        WeddingPlanner.objects.create(
            wedding=wedding,
            planner=planner,
            primary=True,
            read_only=False
        )
        serializer = WeddingSerializerShallow(wedding)
        return Response(serializer.data)
    
    def update(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        wedding = Wedding.objects.get(pk=pk)
        try:
            WeddingPlanner.objects.filter(planner=planner, wedding=wedding)
            wedding.venue=request.data["venue"]
            wedding.name=request.data["name"]
            wedding.save()
            serializer = WeddingUpdateSerializer(wedding)
            return Response(serializer.data)
        except WeddingPlanner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        uid=request.META['HTTP_AUTHORIZATION']
        try:
            planner = Planner.objects.get(uid=uid)
            wedding = Wedding.objects.filter(pk=pk, planner_id=planner)
            wedding.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Planner.DoesNotExist:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['get'], detail=True)
    def guests(self, request, pk):
        planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        try:
            __wedding = Wedding.objects.get(pk=pk)
            try:
                wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
                wedding.guests = Guest.objects.filter(wedding=__wedding)
                for guest in wedding.guests:
                    guest.seated = len(TableGuest.objects.filter(
                        guest_id=guest
                    )) > 0
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
            try:
                wedding = WeddingPlanner.objects.get(planner=planner, wedding=__wedding)
                wedding.reception_tables = ReceptionTable.objects.filter(wedding=__wedding)
                for reception_table in wedding.reception_tables:
                    reception_table.full = len(TableGuest.objects.filter(
                        reception_table_id=reception_table
                    )) > reception_table.capacity
                serializer = TableListSerializer(wedding)
                return Response(serializer.data)
            except WeddingPlanner.DoesNotExist:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
