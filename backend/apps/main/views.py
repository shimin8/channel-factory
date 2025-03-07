from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['GET'])
def serverHealth(req):
    return Response({"msg": "server up and running!"});

@api_view(['GET'])
def fetchLocation(req):
    return Response({"msg": "Route working"})