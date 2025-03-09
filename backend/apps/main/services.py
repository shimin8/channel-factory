from rest_framework.response import Response
from asgiref.sync import sync_to_async
from geopy.distance import geodesic
from .models import Location
from math import radians, cos, sin, asin, sqrt

import httpx
import os
import re

class Service:
    async def fetchLocationAsync(req):

        # normalizing the address received in request body
        normalizedAddress = Service.getNormalizedString(req.data['location'], '+')

        if not normalizedAddress:
            return Response({ 'status': 400, 'error': 'Something went wrong while Normalizing Address' })
        
        # fetch data from postgres database
        results = await sync_to_async(list)(Location.objects.filter(normalized_address=normalizedAddress))

        # if the normalized address is found in our postgres database, we return the result
        if results:
            data = [{
                "formattedAddress": loc.formatted_address,
                "coordinates": {
                    "lat": loc.lat,
                    "lng": loc.lng
                }
            } for loc in results]
            return Response({ 'status': 201, 'data': data[0] })

        # if data not found in database make the google maps api call
        url = os.getenv('GMAPS_GEOCODE_URL') + 'geocode/json?address=' + normalizedAddress + '&key=' + os.getenv('GMAPS_API_KEY')
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

                # saving the new location in the postgres database for future reference
                newLocation = Location(
                    normalized_address=normalizedAddress,
                    formatted_address=respJson['results'][0]['formatted_address'],
                    lat=respJson['results'][0]['geometry']['location']['lat'],
                    lng=respJson['results'][0]['geometry']['location']['lng']
                )
                await sync_to_async(newLocation.save)()

                return Response({ 'status': resp.status_code, 'data': returnResp })

            # handling all the exceptions
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


    async def calcGeoDistanceAsync(req):
        try:
            source = req.data['source']
            req.data['location'] = source
            srcLocation = await Service.fetchLocationAsync(req)

            destination = req.data['destination']
            req.data['location'] = destination
            destLocation = await Service.fetchLocationAsync(req)

            srcCd = (srcLocation.data['data']['coordinates']['lat'], srcLocation.data['data']['coordinates']['lng'])
            destCd = (destLocation.data['data']['coordinates']['lat'], destLocation.data['data']['coordinates']['lng'])

            geoDist = Service.calcGeoDistanceBetweenCoordinates(srcCd, destCd) ## custom distance calculation function
            
            ## for more accuracy
            # geoDist = round(geodesic(srcCd, destCd).kilometers, 2)

            src = srcLocation.data['data']['formattedAddress'],
            dest = destLocation.data['data']['formattedAddress'],

            return Response({ 'status': 200, 'src': src[0], 'dest': dest[0], 'distance': geoDist })

        except Exception as e:
            return Response({ 'error': f'Unexpected error: {str(e)}' }, status = 500)


    def calcGeoDistanceBetweenCoordinates(src, dest):
        try:
            
            srcLat, srcLng, destLat, destLng = map(radians, [src[0], src[1], dest[0], dest[1]])
            
            # using the haversine formula here
            diffLat = destLat - srcLat
            diffLng = destLng - srcLng
            a = sin(diffLat/2)**2 + cos(srcLat) * cos(destLat) * sin(diffLng/2)**2
            b = 2 * asin(sqrt(a))
            r = 6378 # radius of earth in kms at equator
            
            return round(b * r, 2)

        except Exception as e:
            return e
    

    def getNormalizedString(str, ch):
        str = str.lower()
        str = re.sub(r'[^\w\s]', '', str) # removing characters except any word or space characters
        str = re.sub(r'\s+', ch, str).strip() # replacing multiple space characters with the character passed (here '+')
        return str