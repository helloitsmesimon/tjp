import requests
import json
import pandas as pd
import numpy as np
from gpx_converter import Converter

def get_location_info(city, street, street_no=None):
    location = ((str(street_no) + "+") if street_no is not None else "") + street.replace(" ", "+") + ",+" + city
    location = location.replace(' ','').lower()
    resp = requests.get(f'https://nominatim.openstreetmap.org/search?q={location}&format=json&polygon=1&addressdetails=0')
    if resp.status_code != 200:
        raise "Invalid request"
    
    return resp.content
    
def get_coords(city, street, street_no=None):
    j = json.loads(get_location_info(city, street, street_no))
    return j[0]['lat'], j[0]['lon']

coords = [
    get_coords(street="Dreisamstrasse", city="Freiburg"), 
    get_coords(street="Bismarckallee", city="Freiburg"), 
    get_coords(street="Breisacher Strasse", city="Freiburg"), 
    get_coords(street="Eschholzstrasse", city="Freiburg"),
    get_coords(street="Günterstalstrasse", city="Freiburg"), 
    get_coords(street="Habsburgerstrasse", city="Freiburg"), 
    get_coords(street="Leopoldring", city="Freiburg"), 
    get_coords(street="Lorettostrasse", city="Freiburg"), 
    get_coords(street="Stadtstrasse", city="Freiburg"), 
    get_coords(street="Talstrasse", city="Freiburg"), 
    get_coords(street="Waldkircherstrasse", city="Freiburg"), 
    get_coords(street="Kartäuserstrasse", city="Freiburg"),
    get_coords(street="Möslestrasse", city="Freiburg"),
    get_coords(street="Zähringerstrasse", street_no=12, city="Freiburg")
    ]


config = dict()

def get_trip(coordinates, profile='biking'):
    encoded_coords = ";".join([f'{lat},{lon}' for lat, lon in coordinates])
    resp = requests.get(f'''http://router.project-osrm.org/trip/v1/{profile}/{encoded_coords}?steps=false&geometries=polyline&overview=full&annotations=true''')
    if resp.status_code != 200:
        raise "Invalid request"
    
    return json.loads(resp.content)

def get_table(coordinates, profile='foot'):
    encoded_coords = ";".join([f'{lat},{lon}' for lat, lon in coordinates])
    resp = requests.get(f'''http://router.project-osrm.org/table/v1/{profile}/{encoded_coords}''')
    if resp.status_code != 200:
        raise "Invalid request"
    
    return json.loads(resp.content)['durations']

table = get_table(coords)

for i in range(len(coords)):
    table[i][i] = np.inf

def rm_column(arr, i):
    for j in range(len(coords)):
        arr[j][i] = np.inf

i = 0
trip = []
for _ in range(len(coords)):
    trip.append(i)
    rm_column(table, i)
    i = np.argmin(table[i])



def full_result_to_coords(trip):
    # uses location from the trip
    return [coords[wp] for wp in trip]

trip = full_result_to_coords(trip)
df = pd.DataFrame(columns=['latitude','longitude'], data=trip)
print(df)

Converter.dataframe_to_gpx(input_df=df, output_file="test.gpx")
