from gpx_helper import create_gpx_file
from location_types import TourGuide, Waypoint

def main():

    waypoints = [
        Waypoint.from_args(comment="On the fence of the soccer field", street="Dreisamstrasse", street_no=25, city="Freiburg"),
        # Waypoint.from_args(comment="On the fence of the soccer field", street="Freiburger Landstrasse", street_no=25, city="Freiburg-Tiengen"), 
        # Waypoint.from_args(comment="On the fence of the soccer field", street="Gerhart-Hauptmann-Straße", street_no=25, city="Mainz-Gonsenheim"), 
        Waypoint.from_args(comment="On the wall of the bakery", street="Dreisamstrasse", street_no=1, city="Freiburg"), 
        Waypoint.from_args(comment="On the bridge over the river", street="Bismarckallee", city="Freiburg"), 
        Waypoint.from_args(comment="On the bulletin board of the library", street="Breisacher Strasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the door of the cinema", street="Eschholzstrasse", city="Freiburg"),
        Waypoint.from_args(comment="On the lamp post near the park", street="Günterstalstrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the window of the florist", street="Habsburgerstrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the bus shelter at the intersection", street="Leopoldring", city="Freiburg"), 
        Waypoint.from_args(comment="On the gate of the cemetery", street="Lorettostrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the mailbox of the post office", street="Stadtstrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the sign of the hotel", street="Talstrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the fence of the school", street="Waldkircherstrasse", city="Freiburg"), 
        Waypoint.from_args(comment="On the bench of the church", street="Kartäuserstrasse", city="Freiburg"),
        Waypoint.from_args(comment="On the tree of the forest", street="Möslestrasse", city="Freiburg"),
        Waypoint.from_args(comment="On the balcony of the apartment", street="Zähringerstrasse", street_no=12, city="Freiburg")
    ]

    guide = TourGuide(waypoints, profile="bike")  # other profiles are bugged

    # track = guide.compute_greedy_roundtrip()
    track = guide.compute_roundtrip()
    create_gpx_file(track, waypoints, gpx_name="tjp_track")


if __name__ == "__main__":
    main()
