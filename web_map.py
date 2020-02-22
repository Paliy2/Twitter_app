import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os


def generate_map(name_loc, map_name):
    '''
    dict -> ()
    {name: loc}
    '''

    map = folium.Map()
    name_layer = folium.FeatureGroup(name="name's layer")
    for key in name_loc.keys():
        name_layer.add_child(folium.Marker(location=name_loc[key],
                                           tooltip=key))
    map.add_child(name_layer)
    map.add_child(folium.LayerControl())
    map.save('mysite/{}'.format(map_name))

    print('Check map in tests/Map.html')


def get_coordinates(data):
    '''
    dict -> list
    Transfer every location name into coordinates
    '''

    # create geolocator
    geolocator = Nominatim(user_agent="Romanyk", timeout=3)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)

    all_locs = {}
    for key in data.keys():
        location = geocode(data[key])

        if location:
            all_locs[key] = (location.latitude, location.longitude)
    return all_locs


def create_map(data, map_name):
    # data = json_to_dict(file)
    data = get_coordinates(data)
    generate_map(data, map_name)
