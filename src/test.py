import osrm
import requests
import json
import pandas as pd
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
# coords = [
#     get_coords(street="Dreisamstrasse", city="Freiburg"), 
#     get_coords(street="Bärenweg", city="Freiburg"), 
#     get_coords(street="Sundgauallee", city="Freiburg"), 
#     get_coords(street="Eschholzstrasse", city="Freiburg"),
#     get_coords(street="Krozinger Strasse", city="Freiburg")
#     ]

osrm.RequestConfig.profile = "biking"
osrm.RequestConfig.host = "http://router.project-osrm.org"

full_result = osrm.trip([(float(lat), float(lon)) for lat, lon in coords],annotations='true')
def full_result_to_coords(trip):
    # uses location from the trip
    return [w['location'] for w in trip["waypoints"]]

# result = osrm.trip(coords, output = "only_index")
def result_to_coords(trip):
    # uses original waypoints
    return [coords[w["waypoint_index"]] for w in trip['waypoints']]

# trip = result_to_coords(result)
trip = result_to_coords(full_result)
df = pd.DataFrame(columns=['latitude','longitude'], data=trip)
print(df)

Converter.dataframe_to_gpx(input_df=df, output_file="test.gpx")