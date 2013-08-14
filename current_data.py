import urllib
import datetime
import os
import time

while True:
	current_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.json'
	current_file_name = './DownloadedData/' + current_file_name
	if not os.path.exists(current_file_name):
		print "Downloading file... then sleeping."
		urllib.urlretrieve ("http://divvybikes.com/stations/json", current_file_name)
	else:
		print "File already exists. Sleeping"
	time.sleep(30)
