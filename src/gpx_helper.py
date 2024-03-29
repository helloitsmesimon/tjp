from location_types import Waypoint, Coordinate


def create_gpx_file(track: list[Coordinate], waypoints: list[Waypoint], gpx_name: str, track_name: str="Path", track_type: str="Cycle"):
    gpx_header = ''
    gpx_header += f'''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n'''
    gpx_header += f'''<gpx version="1.1" creator="helloitsmesimon@github" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n'''
    gpx_header += f'''<metadata>\n'''
    gpx_header += f'''<name>{gpx_name}</name>\n'''
    gpx_header += f'''</metadata>\n'''

    gpx_track = ''
    gpx_track += f'''<trk>\n'''
    gpx_track += f'''    <name>{track_name}</name>\n'''
    gpx_track += f'''    <type>{track_type}</type>\n'''
    gpx_track += f'''    <trkseg>\n'''
    for step in track:
        gpx_track += f'''    <trkpt lat="{step.latitude}" lon="{step.longitude}"></trkpt>\n'''
    gpx_track += '''    </trkseg>\n</trk>\n'''


    gpx_waypoints = ''
    for waypoint in waypoints:
        gpx_waypoints += f'''<wpt lat="{waypoint.coordinate.latitude}" lon="{waypoint.coordinate.longitude}">\n'''
        gpx_waypoints += f'''    <name>{waypoint.name}</name>\n'''
        gpx_waypoints += f'''    <cmt>{waypoint.comment}</cmt>\n'''
        gpx_waypoints += f'''    <desc>{waypoint.description}</desc>\n'''
        gpx_waypoints += f'''    <sym> </sym>\n'''
        gpx_waypoints += f'''</wpt>\n'''


    gpx_footer = '''</gpx>'''

    gpx_content = gpx_header + gpx_track + gpx_waypoints + gpx_footer

    with open(f'{gpx_name}.gpx', 'w') as file:
        file.write(gpx_content)


def main():
    wps = [Waypoint(coordinates=Coordinate(latitude=48.703037, longitude=10.938682), name="wp1", description="desc1", comment="Wow this one is nice!"),
           Waypoint(coordinates=Coordinate(latitude=48.650828, longitude=11.065179), name="wp2", description="desc2"),
           Waypoint(coordinates=Coordinate(latitude=48.560527, longitude=11.061123), name="wp3", description="desc3"),]

    gpx_name = "TestGPX"

    create_gpx_file(track=[Coordinate(latitude=48.703037, longitude=10.938682), Coordinate(latitude=48.53037, longitude=10.868682)], waypoints=wps, gpx_name=gpx_name)

if __name__ == "__main__":
    main()