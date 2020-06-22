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

"""A simple web server for browsing crowdedness data."""

import flask
import json
import pymongo


app = flask.Flask(__name__)

client = pymongo.MongoClient()
db = client.riskmap


@app.route('/')
def show_root():
  """Renders the user interface."""
  return flask.send_from_directory('../static', 'riskmap.html')


@app.route('/places/<lat>/<lon>')
def read_places(lat, lon):
  """Returns place data near the given location, ordered by distance."""
  places = db.places.find({
    'location': {
      '$near': {
        '$geometry': {
          'type': 'Point',
          'coordinates': [float(lon), float(lat)]
        }
      }
    }
  })
  limit = flask.request.args.get('limit')
  limit = int(limit) if limit else 10
  output = []
  for place in places[:limit]:
    del place['_id']
    output.append(place)
  serialized = json.dumps(output)
  response = flask.make_response(serialized)
  response.headers.set('Content-Type', 'application/json')
  return response


@app.route('/places/<s>/<w>/<n>/<e>')
def read_places_bounds(s, w, n, e):
  """Returns places within the bounds, ordered by distance from the center."""
  limit = flask.request.args.get('limit')
  limit = int(limit) if limit else 10
  lat = (float(n) + float(s)) / 2
  lng = (float(e) + float(w)) / 2
  places = db.places.aggregate([
    {
      '$geoNear': {
        'near': {
          'type': 'Point',
          'coordinates': [lng, lat]
        },
        'distanceField': 'dist.calculated'
      }
    },
    {
      '$limit': limit
    },
    {
      '$match': {
        'location': {
          '$geoWithin': {
            '$box': [
              [float(w), float(s)],
              [float(e), float(n)]
            ]
          }
        }
      }
    }
  ])
  output = []
  for place in places:
    del place['_id']
    output.append(place)
  serialized = json.dumps(output)
  response = flask.make_response(serialized)
  response.headers.set('Content-Type', 'application/json')
  return response


@app.route('/static/<name>')
def read_static(name):
  return flask.send_from_directory('../static', name)


@app.after_request
def prevent_caching(response):
  """Prevents caching any of this app's resources on the client."""
  response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  response.headers['Cache-Control'] = 'public, max-age=0'
  return response
