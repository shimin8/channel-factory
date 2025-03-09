from rest_framework.response import Response
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync

from .services import Service

@api_view(['GET'])
def server_health(req):
    return Response({ 'msg': 'server up and running!'})

@api_view(['POST'])
def fetch_location(req):
    return async_to_sync(Service.fetch_location_async)(req)

@api_view(['POST'])
def calc_geo_distance(req):
    return async_to_sync(Service.calc_geo_distance_async)(req)
