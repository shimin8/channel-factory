from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import httpx
from asgiref.sync import async_to_sync
from geopy.distance import geodesic
import os

mapsBaseUrl = 'https://maps.googleapis.com/maps/api/'

@api_view(['GET'])
def serverHealth(req):
    return Response({ 'msg': 'server up and running!'})



@api_view(['POST'])
def fetchLocation(req):
    return async_to_sync(fetchLocationAsync)(req)

async def fetchLocationAsync(req):

    address = req.data['location'].replace(',', ' ')
    address = address.replace('-', ' ')
    address = address.replace(' ', '+')

    if not address:
        return Response({ 'status': 400, 'error': 'Location is required!!!' })

    url = mapsBaseUrl + 'geocode/json?address=' + address + '&key=' + os.getenv('GMAPS_API_KEY')
    headers = {
        'Accept': 'application/json',
    }

    # setting timeout
    timeout = httpx.Timeout(10.0, connect=5.0, read=5.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(url, headers = headers)
            
            resp.raise_for_status()
            respJson = resp.json()

            returnResp = {
                'formattedAddress': respJson['results'][0]['formatted_address'],
                'coordinates': respJson['results'][0]['geometry']['location']
            }
            return Response({ 'status': resp.status_code, 'data': returnResp })

        except httpx.HTTPStatusError as e:
            return Response({ 'error': f'HTTP error: {e.response.status_code} - {e.response.text}' }, status = e.response.status_code)

        except httpx.ConnectTimeout:
            return Response({ 'error': 'Connection timeout! The server took too long to respond.' }, status = 408)

        except httpx.ReadTimeout:
            return Response({ 'error': 'Read timeout! The server did not send data in time.' }, status = 504)

        except httpx.RequestError as e:
            return Response({ 'error': f'Network error: {e}' }, status = 503)

        except Exception as e:
            return Response({ 'error': f'Unexpected error: {str(e)}' }, status = 500)



@api_view(['POST'])
def calcGeoDistance(req):
    return async_to_sync(calcGeoDistanceAsync)(req)

async def calcGeoDistanceAsync(req):
    try:
        source = req.data['source']
        req.data['location'] = source
        sourceCoordinates = await fetchLocationAsync(req)

        dest = req.data['destination']
        req.data['location'] = dest
        destCoordinates = await fetchLocationAsync(req)

        srcCd = (sourceCoordinates.data['data']['coordinates']['lat'], sourceCoordinates.data['data']['coordinates']['lng'])
        destCd = (destCoordinates.data['data']['coordinates']['lat'], destCoordinates.data['data']['coordinates']['lng'])

        geoDist = geodesic(srcCd, destCd).kilometers

        return Response({ 'status': 200, 'data': geoDist })
    
    except Exception as e:
        return Response({ 'error': f'Unexpected error: {str(e)}' }, status = 500)