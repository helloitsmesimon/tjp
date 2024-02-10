def create_gpx_file(coordinates, waypoint_names, gpx_name):
    if len(coordinates) != len(waypoint_names) or len(coordinates) == 0:
        raise ValueError("Number of coordinates and waypoint names should match and be greater than 0.")

    gpx_header = '''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<gpx version="1.1" creator="Kurviger App" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>{}</name>
  </metadata>'''
    gpx_footer = '''</gpx>'''

    gpx_waypoints = ''
    for coord, name in zip(coordinates, waypoint_names):
        gpx_waypoints += f'  <rte>\n    <name>{name}</name>\n    <rtept lat="{coord[0]}" lon="{coord[1]}" />\n  </rte>\n'

    gpx_content = gpx_header.format(gpx_name) + gpx_waypoints + gpx_footer

    with open(f'{gpx_name}.gpx', 'w') as file:
        file.write(gpx_content)

coordinates = [
    (48.703037, 10.938682),
    (48.650828, 11.065179),
    (48.560527, 11.061123)
]
waypoint_names = [
    "TestName1",
    "TestName2",
    "TestName3"
]
gpx_name = "TestGPX"

create_gpx_file(coordinates, waypoint_names, gpx_name)