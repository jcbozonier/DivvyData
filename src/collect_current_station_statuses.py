import urllib
import datetime
import os
import time
import socket 
socket.setdefaulttimeout(20)

while True:
	current_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.json'
	data_folder = './DownloadedData/'
	current_file_path = data_folder + current_file_name
	try:
		if not os.path.exists(current_file_path):
			print "Downloading file... then sleeping."
			urllib.urlretrieve ("http://divvybikes.com/stations/json", current_file_path)
			f = open(data_folder + 'current_file.txt','w')
			f.write(current_file_name)
		else:
			print "File already exists. Sleeping"
	except:
		 time.sleep(3)
		 continue
	time.sleep(30)