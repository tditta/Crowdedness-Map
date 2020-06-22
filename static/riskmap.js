/**
 * Copyright 2020 Crowdedness Map Authors
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *      http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
let map;
let sw, ne;
let marker;
let infoWindow;

function init() {
  const div = document.getElementById("map");
  const options = {
      zoom: 13,
      streetViewControl: false,
      fullscreenControl: false,
      mapTypeControl: false};
  map = new google.maps.Map(div, options);
  // centerMap();
  map.setCenter({lat: 41.795, lng: -87.588});
  initSearch();
  initMapUpdater();
}

function centerMap() {
  if (!navigator.geolocation) {
    handleLocationError("Browser doesn't support geolocation.");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      map.setCenter({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude});
    });
}

function initSearch() {
  let input = document.getElementById("search");
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  let autocomplete = new google.maps.places.Autocomplete(input, {});
  autocomplete.addListener("place_changed", () => {
    let place = autocomplete.getPlace();
    if (place.geometry) {
      map.panTo(place.geometry.location);
      map.setZoom(15);
    }
  });
}

async function initMapUpdater() {
  map.addListener("idle", async () => {
    if (!hasMoved()) {
      return;
    }
    const bounds = map.getBounds();
    const places = await getPlaces(
        bounds.getSouthWest(), bounds.getNorthEast());
    updateTable(places);
  });
}

function setMarker(place) {
  if (marker) {
    marker.setMap(null);
  }
  if (!place) {
    return;
  }
  const coords = place.location.coordinates;
  const position = {lat: coords[1], lng: coords[0]};
  marker = new google.maps.Marker({
      position: position, animation: google.maps.Animation.DROP});
  marker.setMap(map);
}

function updateTable(places) {
  $("#places tr").remove();
  if (places.length == 0) {
    $("#places").hide();
    $("#placesPlaceholder").show();
    return;
  }
  $("#places").show();
  $("#placesPlaceholder").hide();
  places.forEach(place => {
    const row = $("#placeTemplate tr").clone();
    row.removeAttr("id");
    row.click(() => {
      if (row.attr("selected")) {
        setMarker(null);
        showInfoWindow(null);
        select(null);
      } else {
        setMarker(place);
        showInfoWindow(place);
        select(row);
      }
    });
    $(".placeName", row).text(place.name);
    const icon = getCrowdIcon(place);
    $(".placeIcon img", row).attr("src", icon);
    $("#places").append(row);
  });
}

function select(row) {
  $("#places tr").css("background", "none").removeAttr("selected");
  if (row) {
    row.css("background", "lightblue");
    row.attr("selected", true);
  }
}

function showInfoWindow(place) {
  if (!marker) {
    return;
  }
  if (infoWindow) {
    infoWindow.close();
    infoWindow = null;
  }
  if (!place) {
    return;
  }
  const days = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays",
      "Fridays", "Saturdays"];
  const worstDay = place.dofw[0];
  const worstHour = place.hofd[0];
  if ((worstHour < 0) && (worstDay < 0)) {
    return;
  }
  let text = null;
  if ((worstHour < 0) && (worstDay >= 0)) {
    text = "This place is most crowded<br>on " + days[worstDay] + ".";
  } else if ((worstHour >= 0) && (worstDay < 0)) {
    text = "This place is most crowded<br>between " + worstHourText(worstHour);
  } else {
    text = "This place is most crowded on " + days[worstDay] + "<br>" +
        "and between " + worstHourText(worstHour);
  }
  text = "<center>" + text + "</center>";
  infoWindow = new google.maps.InfoWindow({content: text});
  infoWindow.open(map, marker);
}

function worstHourText(worstHour) {
  if (worstHour == 0) {
    return "12 and 1 a.m.";
  }
  if (worstHour < 11) {
    return worstHour + " and " + (worstHour + 1) + " a.m.";
  }
  if (worstHour == 11) {
    return "11 a.m. and 12 p.m.";
  }
  if ((worstHour > 11) && (worstHour < 23)) {
    return "" + worstHour + " and " + (worstHour + 1) + " p.m.";
  }
  return "11 p.m. and 12 a.m.";
}

function getCrowdIcon(place) {
  const rank = place.crowded_place;
  switch (place.place_tritile) {
    case 0:
      return "/static/person.png";
    case 1:
      return "/static/people.png";
    case 2:
      return "/static/crowd.png";
  }
  return "/static/unknown.png";
}

// If the map's bounds have changed, return true and update the globals.
function hasMoved() {
  const bounds = map.getBounds();
  if (bounds.getSouthWest().equals(sw) && bounds.getNorthEast().equals(ne)) {
    return false;
  }
  sw = bounds.getSouthWest();
  ne = bounds.getNorthEast();
  return true;
}

function handleLocationError(message) {
  const infoWindow = new google.maps.InfoWindow();
  const pos = map.getCenter();
  infoWindow.setPosition(pos);
  infoWindow.setContent(message);
  infoWindow.open(map);
}

function getPlaces(sw, ne) {
  const s = sw.lat();
  const w = sw.lng();
  const n = ne.lat();
  const e = ne.lng();
  return new Promise(resolve => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/places/" + s + "/" + w + "/" + n + "/" + e + "?limit=20");
    xhr.onload = function (event) {
      const places = JSON.parse(xhr.response);
      resolve(places);
    };
    xhr.send();
  });
}
