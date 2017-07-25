import requests


def get_location(lat, lon):
    location_data = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true'.format(lat, lon))

    json = location_data.json()['results'][0]['formatted_address']
    print(json)

get_location(14, 14.5)

file = open('example_data.txt')
lines = file.readlines()
locations = []
for line in lines:
    splitted = line.split(',')
    lat = splitted[0]
    lon = splitted[1]
    print(lat, lon)
    location = get_location(lat,lon)
    locations.append()