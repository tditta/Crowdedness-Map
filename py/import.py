#!/usr/bin/env python

"""
Transform a CSV into GeoJSON suitable for import to MongoDB.

MongoDB can transform GeoJSON into a geospatial index. Import like this:

  $ mongoimport --db riskmap --collection places --drop --file ./Fake-Data/fake_data.json

Then create the index like this:

  > use riskmap
  > db.places.createIndex( { location : "2dsphere" } )

A simple Geospatial query looks like this (longitude first):

  > db.places.find({location: {$geoNear:
        {$geometry: {type: 'Point', coordinates: [-87.584579, 41.799873]}}}})

The CSV schema is described at https://github.com/tditta/Crowdedness-Map.
"""

import csv
import json


def map_int(values):
  out = []
  for v in values:
    if v != '':
      out.append(int(float(v)))
    else:
      out.append(-1)
  return out


with open('Fake-Data/fake_data.csv') as infile:
  with open('Fake-Data/fake_data.json', 'w') as outfile:
    reader = csv.reader(infile)
    reader.__next__()
    for row in reader:
      name = row[0]
      lat, lon = map(float, row[1:3])
      is_grocery, is_restaurant, is_unreliable = map(bool, row[3:6])
      (place_tritile, grocery_tritile, restaurant_tritile,
          relative_tritile) = map_int(row[6:10])
      hofd = map_int(row[10:16])
      dofw = map_int(row[16:])
  
      place = {'name': name}
  
      place['location'] = {'type': 'Point', 'coordinates': [lon, lat]}
  
      place['is_grocery'] = is_grocery
      place['is_restaurant'] = is_restaurant
      place['is_unreliable'] = is_unreliable
      
      place['place_tritile'] = place_tritile
      place['grocery_tritile'] = grocery_tritile
      place['restaurant_tritile'] = restaurant_tritile
      place['relative_tritile'] = relative_tritile
  
      place['hofd'] = hofd
      place['dofw'] = dofw
  
      outfile.write('%s\n' % json.dumps(place))
