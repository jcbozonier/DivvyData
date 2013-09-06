import json
import glob
from datetime import datetime
import csv

#'2013-08-18 11:55:01 PM'

# station_id, group_id, hour, minute, weekend, day_of_week, available_bike_count, available_dock_count
station_entries = []
for file_path in glob.glob("LargeDivvySample/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
	events = json.loads('[' + json_text + ']')
	daily_available_bike_pdfs = {}
	daily_available_dock_pdfs = {}
	for event in events:
		event_date = datetime.strptime(event['executionTime'], '%Y-%m-%d %I:%M:%S %p')
		for station_data in event['stationBeanList']:
			key = (station_data['id'], event_date.hour, event_date.weekday() + 1)
			if not key in daily_available_bike_pdfs:
				daily_available_bike_pdfs[key] = [0]*100
			if not key in daily_available_dock_pdfs:
				daily_available_dock_pdfs[key] = [0]*100
			daily_available_bike_pdfs[key][station_data['availableBikes']] += 1 
			daily_available_dock_pdfs[key][station_data['availableDocks']] += 1
	csv_ready_daily_available_bike_pdfs = [{'station_id': item[0][0], 'hour':item[0][1], 'weekday':item[0][2], 'available_bikes':item[1]} for item in daily_available_bike_pdfs.items()]
	csv_ready_daily_available_dock_pdfs = [{'station_id': item[0][0], 'hour':item[0][1], 'weekday':item[0][2], 'available_docks':item[1]} for item in daily_available_dock_pdfs.items()]
with open('daily_available_bike_pdfs.csv', 'wb') as f: 
	writer = csv.DictWriter(f, ['station_id', 'hour', 'weekday', 'available_bikes'])
	writer.writeheader()
	writer.writerows(csv_ready_daily_available_bike_pdfs)
with open('daily_available_dock_pdfs.csv', 'wb') as f: 
	writer = csv.DictWriter(f, ['station_id', 'hour', 'weekday', 'available_docks'])
	writer.writeheader()
	writer.writerows(csv_ready_daily_available_dock_pdfs)
			
	#print events
 