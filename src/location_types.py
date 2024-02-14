import requests
import json
import numpy as np
from pydantic import BaseModel

OSM_API = '''http://router.project-osrm.org'''
LOCATION_SERVICE_API = '''https://nominatim.openstreetmap.org'''

Coordinates = tuple[str, str]

class Waypoint(BaseModel):
    coordinates: Coordinates
    name: str
    description: str
    comment: str="No Comment"

    def from_args(city: str, street: str, street_no: int | None=None, description: str="", comment: str="", name=""):
        kwargs = locals()
        kwargs['coordinates'] = _get_coords(city=city, street=street, street_no=street_no)
        if name == "":
            kwargs['name'] = street
        return Waypoint(**kwargs)
    
def _get_coords(city, street, street_no=None):
    j = json.loads(_get_location_info(city, street, street_no))
    return j[0]['lat'], j[0]['lon']

def _get_location_info(city: str, street: str, street_no: int | None):
    location = ((str(street_no) + "+") if street_no is not None else "") + street.replace(" ", "+") + ",+" + city
    location = location.replace(' ','').lower()
    resp = requests.get(f'{LOCATION_SERVICE_API}/search?q={location}&format=json&polygon=1&addressdetails=0')
    if resp.status_code != 200:
        raise "Invalid request"

    return resp.content


class TourGuide:
# A TourGuide brings the list of locations in order and organizes a tour while retaining location information
    
    def __init__(self, visits: list[Waypoint], profile: str):
        self.locations = visits
        self.profile = profile

    def _encode_coords_for_osm(self) -> str:
        return ";".join([f'{l.coordinates[0]},{l.coordinates[1]}' for l in self.locations])

    def compute_osm_roundtrip(self):
        encoded_coords = self._encode_coords_for_osm()
        resp = requests.get(f'''{OSM_API}/trip/v1/{self.profile}/{encoded_coords}?steps=false&geometries=polyline&overview=full&annotations=true''')
        if resp.status_code != 200:
            raise "Invalid request"
        
        return json.loads(resp.content)

    def _get_distance_table(self):
        encoded_coords = self._encode_coords_for_osm()
        resp = requests.get(f'''{OSM_API}/table/v1/{self.profile}/{encoded_coords}''')
        if resp.status_code != 200:
            raise "Invalid request"
        
        return json.loads(resp.content)['durations']

    def _get_route(self, from_start, to_finish):
        coordinates = ";".join([f'{l.coordinates[0]},{l.coordinates[1]}' for l in [from_start, to_finish]])
        resp = requests.get(f'''{OSM_API}/route/v1/{self.profile}/{coordinates}?alternatives=false&steps=true&geometries=polyline6&overview=false&annotations=false''')
        if resp.status_code != 200:
            raise "Invalid request"
        steps = json.loads(resp.content)['routes'][0]['legs'][0]['steps']
        coords = [step['maneuver']['location'] for step in steps]

        return coords

    def compute_greedy_roundtrip(self) -> list[Waypoint]:
        order = self._compute_greedy_waypoint_order()

        cur = 0
        path = []
        while cur + 1 < len(order):
            steps = self._get_route(order[cur], order[cur+1])
            print(steps)
            path += steps
            cur += 1

        return path

    def _compute_greedy_waypoint_order(self) -> list[Waypoint]:
        table = self._get_distance_table()
        num_locations = len(self.locations)

        for i in range(num_locations):
            table[i][i] = np.inf

        def rm_column(arr, i):
            for j in range(num_locations):
                arr[j][i] = np.inf

        i = 0
        trip = []
        for _ in range(num_locations):
            trip.append(self.locations[i])
            rm_column(table, i)
            i = np.argmin(table[i])

        return trip
    
