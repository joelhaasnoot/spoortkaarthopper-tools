"""
Convert a list of to/from coordinates and a path to a map of each individual path and an overview
Requires pygmaps
"""
import csv

import sys
import pygmaps

class MapMaker:
    output_dir = ""

    def __init__(self, output):
        self.output_dir = output

    def make_map(self, a, b, point_a, point_b, path):
        # Add to a map and write it out
        path_map = pygmaps.maps(point_a[0], point_a[1], 12)
        path_map.addpoint(point_a[0], point_a[1], "#0000FF")
        path_map.addpoint(point_b[0], point_b[1], "#0000FF")

        # Convert the list
        path_map.addpath(path, "#FF0000")

        path_map.draw('%s/%s-%s.html' % (self.output_dir, a.capitalize(), b.capitalize()));


def decode_line(encoded):
    """
    Decodes a polyline that was encoded using the Google Maps method.

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a straightforward Python port of Mark McClure's JavaScript polyline decoder
    (http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/decode.js)
    and Peter Chng's PHP polyline decode
    (http://unitstep.net/blog/2008/08/02/decoding-google-maps-encoded-polylines-using-php/)
    """

    encoded_len = len(encoded)
    index = 0
    array = []
    lat = 0
    lng = 0

    while index < encoded_len:

        b = 0
        shift = 0
        result = 0

        while True:
            b = ord(encoded[index]) - 63
            index = index + 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat

        shift = 0
        result = 0

        while True:
            b = ord(encoded[index]) - 63
            index = index + 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        array.append((lat * 1e-5, lng * 1e-5))

    return array


def run():
    INPUT_FILE = sys.argv[1]
    OUTPUT_DIR = sys.argv[2]

    paths = []

    m = MapMaker(OUTPUT_DIR)
    with open(INPUT_FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            path = decode_line(row[2])
            path_tup = (row[0], row[1], path)
            paths.append(path_tup)
            m.make_map(row[0], row[1], path[0], path[-1], path)
            #total_map.addpath(list(thelist), "#FF0000") # Also add to our global map with all the pieces


if __name__ == "__main__":
    run()
