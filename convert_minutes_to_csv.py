import json
import glob
from datetime import datetime
import csv

#'2013-08-18 11:55:01 PM'

# station_id, group_id, hour, minute, weekend, day_of_week, available_bike_count, available_dock_count
station_entries = []
for file_path in glob.glob("SampleData/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
	events = json.loads('[' + json_text + ']')
	for event in events:
		event_date = datetime.strptime(event['executionTime'], '%Y-%m-%d %I:%M:%S %p')
		for station_data in event['stationBeanList']:
			station_log_entry = {
				'station_id': station_data['id'],
				'group_id': -1,
				'hour': event_date.hour,
				'minute': event_date.minute,
				'is_weekend': (event_date.weekday() == 6) or (event_date.weekday() == 7),
				'day_of_week': event_date.weekday() + 1,
				'available_bike_count': station_data['availableDocks'],
				'available_dock_count': station_data['availableBikes'],
				'available_bike_percent': round(1.0*station_data['availableDocks']/station_data['totalDocks'], 2),
				'available_dock_percent': round(1.0*station_data['availableBikes']/station_data['totalDocks'], 2)
			}
			station_entries.append(station_log_entry)

with open('processed_station_logs.csv', 'wb') as f: 
	writer = csv.DictWriter(f, station_entries[0].keys())
	writer.writeheader()
	writer.writerows(station_entries)
			
	#print events
 