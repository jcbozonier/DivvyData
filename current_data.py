import urllib
import datetime

current_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.json'
urllib.urlretrieve ("http://divvybikes.com/stations/json", current_file_name)