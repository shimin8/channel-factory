from rest_framework.response import Response
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync

from .services import Service

@api_view(['GET'])
def serverHealth(req):
    return Response({ 'msg': 'server up and running!'})

@api_view(['POST'])
def fetchLocation(req):
    return async_to_sync(Service.fetchLocationAsync)(req)

@api_view(['POST'])
def calcGeoDistance(req):
    return async_to_sync(Service.calcGeoDistanceAsync)(req)
