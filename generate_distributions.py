import json
import glob
from datetime import datetime
import csv

counter = 0
stations = {}
for file_path in glob.glob("andys_data/*.json"):
	counter += 1
	#if counter > 1440:
	#	break
	print "Processing " + file_path + "..."
	json_file = open(file_path)
	json_text = json_file.read().replace(" u'", "'").replace("{u'", "{'").replace("'", "\"").replace(": None", ": \"\"").replace(": False", ": 0").replace(": True", ": 1")
	try:
		minute_data = json.loads(json_text)
	except:
		print "Errored on " + file_path
		continue
	time_text = minute_data['executionTime']
	event_time = datetime.strptime(time_text, '%Y-%m-%d %I:%M:%S %p')
	events = minute_data['stationBeanList']
	for event in events:
		station_id = event["id"]
		weekend = event_time.weekday() >= 5
		hour = event_time.hour
		key = (station_id, weekend, hour)
		if not key in stations:
			stations[key] = {
				'id': station_id,
				'available_docks': [0]*55,
				'available_bikes': [0]*55
			}
		station_info = stations[key]
		station_info['available_bikes'][event['availableBikes']] += 1
		station_info['available_docks'][event['availableDocks']] += 1

available_bikes_by_station = {}
available_docks_by_station = {}

for key in stations.keys():
	station_id = key[0]
	hour = key[2]
	if not station_id in available_bikes_by_station:
		available_bikes_by_station[station_id] = [[0]*55 for i in range(0,24)]
	if not station_id in available_docks_by_station:
		available_docks_by_station[station_id] = [[0]*55 for i in range(0,24)]

	available_bikes_by_station[station_id][hour] = map(lambda le_tuple: le_tuple[0] + le_tuple[1], zip(available_bikes_by_station[station_id][hour], stations[key]['available_bikes']))
	available_docks_by_station[station_id][hour] = map(lambda le_tuple: le_tuple[0] + le_tuple[1], zip(available_docks_by_station[station_id][hour], stations[key]['available_docks']))
station_bikes = []
station_docks = []
for station_id in available_bikes_by_station.keys():
	bike_available_hours = available_bikes_by_station[station_id]
	dock_available_hours = available_docks_by_station[station_id]
	for hour in xrange(0,24):
		bike_available_distribution = bike_available_hours[hour]
		dock_available_distribution = dock_available_hours[hour]
		hours_for_bikes_normalized = [round((1.0*i)/sum(bike_available_distribution), 6) if sum(bike_available_distribution) != 0 else 0 for i in bike_available_distribution]
		station_bikes_hour = [station_id, hour]
		station_bikes_hour.extend(hours_for_bikes_normalized)
		station_bikes.append(station_bikes_hour)
		hours_for_docks_normalized = [round((1.0*i)/sum(dock_available_distribution), 6) if sum(dock_available_distribution) != 0 else 0 for i in dock_available_distribution]
		station_docks_hour = [station_id, hour]
		station_docks_hour.extend(hours_for_docks_normalized)
		station_docks.append(station_docks_hour)

with open('bike_availability_by_station_hour.csv', 'w') as f: 
	writer = csv.writer(f)
	writer.writerows(station_bikes)
with open('bike_availability_by_station_hour.json', 'w') as f: 
	json.dump(station_bikes, f)
with open('dock_availability_by_station_hour.json', 'w') as f: 
	json.dump(station_docks, f)

#station_info_for_csv = [{'station_id': item[0][0], 'weekend': item[0][1], 'hour':item[0][2], 'available_bikes':item[1]['available_bikes'], 'available_docks':item[1]['available_docks']} for item in stations.items()]

#with open('station_distributions.csv', 'wb+') as f: 
#	writer = csv.DictWriter(f, ['station_id', 'weekend', 'hour', 'available_bikes', 'available_docks'])
#	writer.writeheader()
#	writer.writerows(station_info_for_csv)


