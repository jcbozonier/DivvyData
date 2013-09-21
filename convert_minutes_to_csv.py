import json
import glob
from datetime import datetime

#'2013-08-18 11:55:01 PM'

for file_path in glob.glob("SampleData/*.json"):
	json_file = open(file_path)
	json_text = json_file.read()
	events = json.loads('[' + json_text + ']')
	for event in events:
		event_date = datetime.strptime(event['executionTime'], '%Y-%m-%d %I:%M:%S %p')
		print event_date.day
	#print events
 