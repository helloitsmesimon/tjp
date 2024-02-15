import requests
import json
import numpy as np
import polyline
from pydantic import BaseModel

OSM_API = '''http://router.project-osrm.org'''
LOCATION_SERVICE_API = '''https://nominatim.openstreetmap.org'''


class Coordinate(BaseModel):
    latitude: str
    longitude: str 

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude


class Waypoint(BaseModel):
    coordinate: Coordinate
    name: str
    description: str
    comment: str="No Comment"


    def from_args(city: str, street: str, street_no: int | None=None, description: str="", comment: str="", name=""):
        kwargs = locals()
        lat, lon = _resolve_lat_lon(city=city, street=street, street_no=street_no)
        kwargs['coordinate'] = Coordinate(latitude=lat, longitude=lon)
        if name == "":
            kwargs['name'] = street
        return Waypoint(**kwargs)
    

def _resolve_lat_lon(city, street, street_no=None):
    j = _get_location_info(city, street, street_no)
    return j[0]['lat'], j[0]['lon']


def _get_location_info(city: str, street: str, street_no: int | None):
    location = ((str(street_no) + "+") if street_no is not None else "") + street.replace(" ", "+") + ",+" + city
    location = location.replace(' ','').lower()
    resp = requests.get(f'{LOCATION_SERVICE_API}/search?q={location}&format=json&polygon=1&addressdetails=0')
    if resp.status_code != 200:
        raise "Invalid request"

    return json.loads(resp.content)


class TourGuide:
# A TourGuide brings the list of locations in order and organizes a tour while retaining location information
    
    def __init__(self, visits: list[Waypoint], profile: str):
        self.locations = visits
        self.profile = profile


    def _encode_coords_for_osm(self) -> str:
        return ";".join([f'{l.coordinate.longitude},{l.coordinate.latitude}' for l in self.locations])
    

    def _get_osm_roundtrip(self):
        encoded_coords = self._encode_coords_for_osm()
        resp = requests.get(f'''{OSM_API}/trip/v1/{self.profile}/{encoded_coords}?steps=false&geometries=polyline&overview=full&annotations=true''')
        if resp.status_code != 200:
            raise "Invalid request"
        
        return json.loads(resp.content)


    def compute_roundtrip(self) -> list[Coordinate]:
        c = self._get_osm_roundtrip()
        track = [Coordinate(latitude=str(coord[0]), longitude=str(coord[1])) for coord in polyline.decode(c['trips'][0]['geometry'])]
        return track
    