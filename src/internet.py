def coords_to_gpx_track(coords, filename):
    with open(filename, 'w') as f:
        start = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
  <trk>
    <trkseg>
"""
        fill = "\n".join([f'''      <trkpt lat="{coord[0]}" lon="{coord[1]}">
      </trkpt>''' for coord in coords])
        end = """
    </trkseg>
  </trk>
</gpx>"""
        f.write(start + fill + end)

