import json
import glob
from datetime import datetime
import csv

#'2013-08-18 11:55:01 PM'

# station_id, group_id, hour, minute, weekend, day_of_week, available_bike_count, available_dock_count
station_entries = []
station_temperatures = {}
for file_path in glob.glob("LargeDivvySample/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
	events = json.loads('[' + json_text + ']')
	for event in events:
		event_date = datetime.strptime(event['executionTime'], '%Y-%m-%d %I:%M:%S %p')
		for station_data in event['stationBeanList']:
			key = (station_data['id'], event_date.hour, event_date.weekday() + 1)
			if not (key in station_temperatures):
				station_temperatures[key] = {'last_seen_bikes':station_data['availableBikes'], 'bike_increases':0, 'bike_decreases':0}
			if station_temperatures[key]['last_seen_bikes'] < station_data['availableBikes']:
				station_temperatures[key]['bike_increases'] += 1
				station_temperatures[key]['last_seen_bikes'] = station_data['availableBikes']
			if station_temperatures[key]['last_seen_bikes'] > station_data['availableBikes']:
				station_temperatures[key]['bike_decreases'] += 1
				station_temperatures[key]['last_seen_bikes'] = station_data['availableBikes']
csv_ready_station_temperatures = [{'station_id': item[0][0], 'hour':item[0][1], 'weekday':item[0][2], 'time_id': item[0][1] + 24*item[0][2], 'bike_increases':item[1]['bike_increases'], 'bike_decreases':item[1]['bike_decreases']} for item in station_temperatures.items()]
with open('station_temperatures.csv', 'wb+') as f: 
	writer = csv.DictWriter(f, ['station_id', 'hour', 'weekday', 'time_id', 'bike_increases', 'bike_decreases'])
	writer.writeheader()
	writer.writerows(csv_ready_station_temperatures)
			
	#print events
 