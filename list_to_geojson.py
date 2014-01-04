"""
This tool converts output.csv into a GeoJSON blob with each line being a feature
"""
from polyline import *
import json

features = []
with open('output.csv', 'r') as input_file:
	for line in input_file.readlines():
		row = line.split(',')

		obj = { 'type' : 'Feature', 'geometry' : {'type' : 'LineString', 'coordinates' : [] }, 
			'properties' : {'from' : row[0], 'to' : row[1] } }
		obj['geometry']['coordinates'] = decode(row[2])
		features.append(obj)

print json.dumps({'type' : 'FeatureCollection', 'features' : features })
		
