# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from coordinatesapi.models import Planner, Wedding, WeddingPlanner, TableGuest, Guest, ReceptionTable, Group

# class WeddingView(ViewSet):

#     def retrieve(self, request, pk):
#         planner = Planner.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
#         try:
#             wedding = Wedding.objects.get(pk=pk)
#             __wedding = WeddingPlanner.objects.get(planner=planner, wedding=wedding)

#             return Response(serializer.data)
#         except WeddingPlanner.DoesNotExist:
#             return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
#         except Wedding.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
