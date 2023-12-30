/* a lot of this code is from here https://projects.raspberrypi.org/en/projects/wheres-zombie */
/*global google*/
var zombie_map;
var old_position;
var tolerance = 10;
var all_markers = [];
var pathline = [];
//this is a javascript list of markers for the map - line separated and the 3 items in each line are long,lat and icon url
var data = `51.38641974485056 -2.344442034393317 https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fhospital.png
51.387133113126175 -2.345062843817025 https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fzombie.png
51.386881731266 -2.3405152803955143 https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fzombie.png
51.386024709288954 -2.3432618624267643 https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fzombie.png
51.38641974485056 -2.344442034393317 https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fhospital.png`;
//this line turns the data into an array
var markers = data.split("\n");

function initMap() {
  //init the map
  zombie_map = new google.maps.Map(document.getElementById("zombie_map"), {
    zoom: 17,
    center: { lat: 51.386634, lng: -2.344206 }
  });
  //add markers
  for (var i = 0; i < markers.length; i++) {
    console.log(markers[i] + "<br>");
    var marker_data = markers[i].trim();
    marker_data = marker_data.split(" ");
    var latitude = marker_data[0];
    var longitude = marker_data[1];
    var emoji = marker_data[2];

    var marker_position = new google.maps.LatLng(latitude, longitude);
    var marker = new google.maps.Marker({
      position: marker_position,
      map: zombie_map,
      icon: emoji
    });
    
    all_markers.push(marker);
    pathline.push(marker_position)
    /* drawing paths
    https://stackoverflow.com/questions/7891736/how-to-join-all-markers-with-paths-in-google-maps */
    var flightPath = new google.maps.Polyline({
      path: pathline,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    flightPath.setMap(zombie_map)
  }
  zombie_map.addListener("click", function(e) {
    var location = e.latLng;
    placemarker(location); //runs placemarker function every click
  });
}
function placemarker(location) {
  //adds new zombie emoji wherever you click
  var emoji = "https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fzombie.png";
  var marker = new google.maps.Marker({
    position: location,
    map: zombie_map,
    icon: emoji
  });
  console.log(location.lat() + " " + location.lng() + " " + emoji);
}
//This below function was for the mobile game to walk around '"looking" for zombies'
function set_my_position(position) {
  //console.log(position);
  old_position.setMap(null);
  var pos = new google.maps.LatLng(
    position.coords.latitude,
    position.coords.longitude
  );
  //zombie_map.setCenter(pos);
  var me = new google.maps.Marker({
    position: pos,
    map: zombie_map,
    icon:
      "https://cdn.glitch.com/1bf28fcc-9c66-4df1-b451-dfe5f696fac7%2Fsmiley4.png?v=1625063691950"
  });
  old_position = me;
  for (var i = 0; i < all_markers.length; i++) {
    var distance = google.maps.geometry.spherical.computeDistanceBetween(
      pos,
      all_markers[i].getPosition()
    );
    console.log(distance);
    if (distance < tolerance) {
      var what_is_it = all_markers[i].getIcon();
      what_is_it = what_is_it.replace(".png", "");
      alert("Found the " + what_is_it);
      all_markers.setMap(null);
    }
  }
}
