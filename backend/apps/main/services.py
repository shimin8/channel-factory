from rest_framework.response import Response
from asgiref.sync import sync_to_async
from geopy.distance import geodesic
from .models import Location
from math import radians, cos, sin, asin, sqrt

import httpx
import os
import re

class Service:
    async def fetch_location_async(req):

        # normalizing the address received in request body
        normalized_address = Service.get_normalized_string(req.data['location'], '+')

        if not normalized_address:
            return Response({ 'status': 400, 'error': 'Something went wrong while Normalizing Address' })
        
        # fetch data from postgres database
        results = await sync_to_async(list)(Location.objects.filter(normalized_address=normalized_address))

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
        url = os.getenv('GMAPS_GEOCODE_URL') + 'geocode/json?address=' + normalized_address + '&key=' + os.getenv('GMAPS_API_KEY')
        headers = {
            'Accept': 'application/json',
        }

        # setting timeout
        timeout = httpx.Timeout(10.0, connect=5.0, read=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.get(url, headers = headers)
                
                resp.raise_for_status()
                resp_json = resp.json()

                return_resp = {
                    'formattedAddress': resp_json['results'][0]['formatted_address'],
                    'coordinates': resp_json['results'][0]['geometry']['location']
                }

                # saving the new location in the postgres database for future reference
                new_location = Location(
                    normalized_address=normalized_address,
                    formatted_address=resp_json['results'][0]['formatted_address'],
                    lat=resp_json['results'][0]['geometry']['location']['lat'],
                    lng=resp_json['results'][0]['geometry']['location']['lng']
                )
                await sync_to_async(new_location.save)()

                return Response({ 'status': resp.status_code, 'data': return_resp })

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


    async def calc_geo_distance_async(req):
        try:
            source = req.data['source']
            req.data['location'] = source
            src_location = await Service.fetch_location_async(req)

            destination = req.data['destination']
            req.data['location'] = destination
            dest_location = await Service.fetch_location_async(req)

            src_cd = (src_location.data['data']['coordinates']['lat'], src_location.data['data']['coordinates']['lng'])
            dest_cd = (dest_location.data['data']['coordinates']['lat'], dest_location.data['data']['coordinates']['lng'])

            geo_dist = Service.calc_geo_distance_between_coordinates(src_cd, dest_cd) ## custom distance calculation function

            ## for more accuracy
            # geo_dist = round(geodesic(src_cd, dest_cd).kilometers, 2)

            src = src_location.data['data']['formattedAddress'],
            dest = dest_location.data['data']['formattedAddress'],

            return Response({ 'status': 200, 'src': src[0], 'dest': dest[0], 'distance': geo_dist })

        except Exception as e:
            return Response({ 'error': f'Unexpected error: {str(e)}' }, status = 500)


    def calc_geo_distance_between_coordinates(src, dest):
        try:
            
            src_lat, src_lng, dest_lat, dest_lng = map(radians, [src[0], src[1], dest[0], dest[1]])
            
            # using the haversine formula here
            diffLat = dest_lat - src_lat
            diffLng = dest_lng - src_lng
            a = sin(diffLat/2)**2 + cos(src_lat) * cos(dest_lat) * sin(diffLng/2)**2
            b = 2 * asin(sqrt(a))
            r = 6378 # radius of earth in kms at equator
            
            return round(b * r, 2)

        except Exception as e:
            return e
    

    def get_normalized_string(str, ch):
        str = str.lower()
        str = re.sub(r'[^\w\s]', '', str) # removing characters except any word or space characters
        str = re.sub(r'\s+', ch, str).strip() # replacing multiple space characters with the character passed (here '+')
        return str