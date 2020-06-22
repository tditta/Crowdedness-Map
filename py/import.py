#!/usr/bin/env python

# Copyright 2020 Crowdedness Map Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
