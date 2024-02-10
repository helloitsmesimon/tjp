# Traveling Jakob Problem

A person has to visit a few locations one after another. Jakob wants to use a bike to get around and has a smartphone for navigation.

 Create a route that passes a number of given locations. The route should be short and displayable with a common gps app or via browser.

# Technically:

1. Resolve locations to coordinates -> use routing engine (osrm)
2. Compute routes -> osrm's tsp seemed to be bad, so I created a greedy tour (always go to the closest place).
3. Get the route back into some navigation app

# Problems:

Geopackages that use gdal are hard to install. Premade docker images could not be found.
C_INCLUDE_PATH=/usr/include/gdal CPLUS_INCLUDE_PATH=/usr/include/gdal python -m pip install GDAL=="$(gdal-config --version)"
