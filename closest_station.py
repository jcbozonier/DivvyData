# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import json
import urllib
from datetime import datetime

import math

def haversine(lat1, lon1, lat2, lon2):
    R = 3959
    # In miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# <codecell>

json_file = urllib.urlopen('http://www.divvybikes.com/stations/json')
json_text=json_file.read()
current_state = json.loads('[' + json_text + ']')[0]

station_status = []
for station in current_state['stationBeanList']:
	station_status.append({'id':station['id'],'name':station['stationName'], 'bikes':station['availableBikes'],'docks':station['availableDocks'],'lat':station['latitude'],'long':station['longitude']})
        
        

# <codecell>

current_state['stationBeanList'][0]

# <codecell>

current_location={'lat':41.882840,'long':-87.631436}

# <codecell>

haversine(current_location['lat'],current_location['long'],station_status[0]['lat'],station_status[0]['long'])

# <codecell>

closest_station = station_status[0]
closest_station_distance = haversine(current_location['lat'],current_location['long'],station_status[0]['lat'],station_status[0]['long'])
for station in station_status:
    if haversine(current_location['lat'],current_location['long'],station['lat'],station['long'])<closest_station_distance:
        closest_station=station
        
print station
    

