import requests
import json
import numpy as np
import polyline
from pydantic import BaseModel

OSM_API = '''http://router.project-osrm.org'''
LOCATION_SERVICE_API = '''https://nominatim.openstreetmap.org'''


class Step(BaseModel):
    latitude: str
    longitude: str 

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

class Waypoint(BaseModel):
    latitude: str
    longitude: str
    name: str
    description: str
    comment: str="No Comment"

    def from_args(city: str, street: str, street_no: int | None=None, description: str="", comment: str="", name=""):
        kwargs = locals()
        kwargs['latitude'], kwargs['longitude'] = _get_lat_lon(city=city, street=street, street_no=street_no)
        if name == "":
            kwargs['name'] = street
        return Waypoint(**kwargs)
    
def _get_lat_lon(city, street, street_no=None):
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
        return ";".join([f'{l.longitude},{l.latitude}' for l in self.locations])



    def _get_distance_table(self):
        encoded_coords = self._encode_coords_for_osm()
        resp = requests.get(f'''{OSM_API}/table/v1/{self.profile}/{encoded_coords}''')
        if resp.status_code != 200:
            raise "Invalid request"
        
        return json.loads(resp.content)['durations']

    def _get_route(self, from_start, to_finish):
        coordinates = ";".join([f'{l.longitude},{l.latitude}' for l in [from_start, to_finish]])
        resp = requests.get(f'''{OSM_API}/route/v1/{self.profile}/{coordinates}?alternatives=false&steps=true&geometries=polyline6&overview=false&annotations=false''')
        if resp.status_code != 200:
            raise "Invalid request"
        steps = json.loads(resp.content)['routes'][0]['legs'][0]['steps']
        coords = [Step(longitude=str(step['maneuver']['location'][0]), latitude=str(step['maneuver']['location'][1])) for step in steps]
        
        return coords

    def compute_greedy_roundtrip(self) -> list[Waypoint]:
        self._waypoint_roundtrip()
        order = self._compute_greedy_waypoint_order()

        cur = 0
        path = []
        while cur + 1 < len(order):
            steps = self._get_route(order[cur], order[cur+1])
            path += steps
            cur += 1

        path += self._get_route(order[-1], order[0])  # for the roundtrip

        path_without_duplicates = []
        cur = 0
        while cur + 1 < len(path):
            if path[cur] != path[cur+1]:
                path_without_duplicates.append(path[cur])
            cur += 1

        return path_without_duplicates
    
    def _get_osm_roundtrip(self):
        encoded_coords = self._encode_coords_for_osm()
        resp = requests.get(f'''{OSM_API}/trip/v1/{self.profile}/{encoded_coords}?steps=false&geometries=polyline&overview=full&annotations=true''')
        if resp.status_code != 200:
            raise "Invalid request"
        
        return json.loads(resp.content)
    
    def compute_roundtrip(self) -> list[Step]:
        c = self._get_osm_roundtrip()
        # waypoints = [self.waypoints[wp['waypoint_index']] for wp in c['waypoints']]
        track = [Step(latitude=str(coord[0]), longitude=str(coord[1])) for coord in polyline.decode(c['trips'][0]['geometry'])]
        return track


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
    
