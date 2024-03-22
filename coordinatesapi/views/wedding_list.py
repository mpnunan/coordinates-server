from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .wedding import WeddingView
from coordinatesapi.serializers import SortedWeddingSerializer

import json


class WeddingListView(ViewSet):
    def list(self, request):
        __wedding_list = WeddingView.list(self, request)
        wedding_list = __wedding_list.data
        __weddings = json.dumps(wedding_list)
        weddings = json.loads(__weddings)

        primary = []
        read_only = []
        shared = []

        for wedding in weddings:
            if wedding['primary'] is True:
                primary.append(wedding)
            if wedding['read_only'] is True:
                read_only.append(wedding)
            if wedding['primary'] is False and wedding['read_only'] is False:
                shared.append(wedding)

        serializer = SortedWeddingSerializer(
            {'primary': primary, 'read_only': read_only, 'shared': shared})
        return Response(serializer.data)
