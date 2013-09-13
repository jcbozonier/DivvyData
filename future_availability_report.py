import json
import glob
from datetime import datetime, timedelta
import csv

#'2013-08-18 11:55:01 PM'

# station_id, group_id, hour, minute, weekend, day_of_week, available_bike_count, available_dock_count
def subtract_from_date(event_date, minutes_delta):
	return event_date - timedelta(0,minutes_delta*60)

def update_appropriate(the_futures, current_date, station_id, was_bike_available, was_dock_available):
	updates = [{'index_to_update': i, 'time_to_log': subtract_from_date(current_date, i)} for i in xrange(0,26)]
	for update in updates:
		update_date = update['time_to_log']
		key = (station_id, update_date.hour, update_date.minute, update_date.weekday() + 1)
		if key in the_futures:
			the_futures[key]['future_bike_availability'][update['index_to_update']] += 1 if was_bike_available else 0
			the_futures[key]['future_dock_availability'][update['index_to_update']] += 1 if was_dock_available else 0
			the_futures[key]['total_count'][update['index_to_update']] += 1

futures = {}
for file_path in glob.glob("SampleData/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
	events = json.loads('[' + json_text + ']')
	for event in events:
		event_date = datetime.strptime(event['executionTime'], '%Y-%m-%d %I:%M:%S %p')
		for station_data in event['stationBeanList']:
			key = (station_data['id'], event_date.hour, event_date.minute, event_date.weekday() + 1)
			if not (key in futures):
				futures[key] = {
					'future_bike_availability': [0]*26,
					'future_dock_availability': [0]*26,
					'total_count': 0
				}
			update_appropriate(futures, event_date, station_data['id'], station_data['availableBikes'] > 0, station_data['availableDocks'] > 0)

csv_ready_future_availability = [{'station_id': item[0][0], 'hour':item[0][1], 'minute':item[0][2], 'weekday':item[0][3], 'time_id': item[0][1] + 24*item[0][3], 'future_bike_availability':item[1]['future_bike_availability'], 'future_dock_availability':item[1]['future_dock_availability']} for item in futures.items()]

with open('future_availability_report.csv', 'wb+') as f: 
	writer = csv.DictWriter(f, ['station_id', 'hour', 'minute', 'weekday', 'time_id', 'future_bike_availability', 'future_dock_availability'])
	writer.writeheader()
	writer.writerows(csv_ready_future_availability)
			
	#print events
 