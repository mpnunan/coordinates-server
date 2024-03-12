from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .wedding import WeddingView
from coordinatesapi.serializers import GuestsSortedSerializer, GuestsUnseatedSerializer
import json


class GuestListView(ViewSet):
    def retrieve(self, request, pk):
        __guest_list = WeddingView.guests(self, request, pk)
        guest_list = __guest_list.data
        __sorted_guest_list = json.dumps(guest_list["guests"])
        sorted_guest_list = json.loads(__sorted_guest_list)

        side = request.query_params.get('side', None)
        if side is not None:
            sorted_guest_list = filter(
                lambda guest: guest['participant'] if str(guest['participant']['id']) == side else None, sorted_guest_list
            )

        family = []
        party = []
        couples = []
        problems = []
        guests = []

        for guest in sorted_guest_list:
            if guest['family'] is True:
                family.append(guest)
            if guest['party'] is True:
                party.append(guest)
            if 'partner' in guest:
                couples.append(guest)
            if 'problem' in guest:
                problems.append(guest)
            if guest['family'] is False and guest['party'] is False and 'partner' not in guest:
                guests.append(guest)

        serializer = GuestsSortedSerializer(
            {'guests': guests, 'family': family, 'party': party, 'couples': couples, 'problems': problems})
        return Response(serializer.data)

class UnseatedGuestView(ViewSet):
    def retrieve(self, request, pk):
        __guest_list = WeddingView.guests(self, request, pk)
        guest_list = __guest_list.data
        __all_guests = json.dumps(guest_list["guests"])
        all_guests = json.loads(__all_guests)
        guests = []
        for guest in all_guests:
            if guest["seated"] is False:
                guests.append(guest)

        serializer = GuestsUnseatedSerializer(
            {'guests': guests, 'length': len(guests)}
        )
        return Response(serializer.data)
