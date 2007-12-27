
function updateMap(event) {
    if (!event) var event = window.event; // IE compatibility
    var latitude = cssQuery("input#geolocation_latitude")[0];
    var longitude = cssQuery("input#geolocation_longitude")[0];
    if (latitude.value != "0.0" && longitude.value != "0.0") {return false};
    var _mapsConfig = mapsConfig;
    var _reb_country = reb_country;
    var _mapsConfig_google = _mapsConfig.google;
    var street = cssQuery('input#title');
    var city = cssQuery('select#city');
    var address = street[0].value + ", " + city[0].value + ", " + _reb_country;

    var location = cssQuery('div.locationString')[0];    
    var map_node = cssQuery('div.googleMapPane')[0];
    
    var _parseSearchResults = function() {
        var place = _mapsLocalSearch.results[0];
        if (place) {
            latitude.value = place.lat;
            longitude.value = place.lng;
            location.innerHTML = place.lat + ", " + place.lng;
            var map = new GMap2(map_node);
            var center = new GLatLng(parseFloat(latitude.value),
                                     parseFloat(longitude.value));
            map.setCenter(center, _mapsConfig_google.initialzoomlevel,
                          G_HYBRID_MAP);
            map.addControl(new GLargeMapControl());
            if (_mapsConfig_google.selectablemaptypes) {
                map.addControl(new GMapTypeControl());
            }
            var $marker = new GMarker(center, {draggable: true});
            map.addOverlay($marker);
            GEvent.addListener($marker, "dragend", function() {
                var point = $marker.getPoint();
                latitude.value = point.lat();
                longitude.value = point.lng();
                $location.innerHTML = point.lat() + ", " + point.lng();
            });
            GEvent.addListener(map, "click", function(overlay, point) {
                if (!overlay) {
                    $marker.setPoint(point);
                    latitude.value = point.lat();
                    longitude.value = point.lng();
                    location.innerHTML = point.lat() + ", " + point.lng();
                }
            });
        }
    };
    _mapsLocalSearch = new GlocalSearch();
    _mapsLocalSearch.setSearchCompleteCallback(
        null, _parseSearchResults
        );
    _mapsLocalSearch.execute(address);
};

function activateMapUpdater() {
    var tabs = cssQuery('li.formTab');
    if (tabs[0] == undefined) {return false;}    
    var idx = tabs.length-1;
    var location_tab = tabs[idx];
    location_tab.onclick = updateMap;
}

registerPloneFunction(activateMapUpdater);

