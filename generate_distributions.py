import json
import glob
from datetime import datetime
import csv

stations = {}
for file_path in glob.glob("JustTheData/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
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
				'available_docks': [0]*150,
				'available_bikes': [0]*150
			}
		station_info = stations[key]
		station_info['available_bikes'][event['availableBikes']] += 1
		station_info['available_docks'][event['availableDocks']] += 1
hours = [[0]*150 for i in range(0,24)]
for key in stations.keys():
	hour = key[2]
	hours[hour] = map(lambda le_tuple: le_tuple[0] + le_tuple[1], zip(hours[hour], stations[key]['available_bikes']))

hours_normalized = []
for distribution in hours:
	hours_normalized.append([(1.0*i)/sum(distribution) for i in distribution])

with open('hour_distributions.csv', 'w') as f: 
	writer = csv.writer(f)
	writer.writerows(hours_normalized)

#station_info_for_csv = [{'station_id': item[0][0], 'weekend': item[0][1], 'hour':item[0][2], 'available_bikes':item[1]['available_bikes'], 'available_docks':item[1]['available_docks']} for item in stations.items()]

#with open('station_distributions.csv', 'wb+') as f: 
#	writer = csv.DictWriter(f, ['station_id', 'weekend', 'hour', 'available_bikes', 'available_docks'])
#	writer.writeheader()
#	writer.writerows(station_info_for_csv)


