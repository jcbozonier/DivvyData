import urllib
import datetime
import time
import json
from boto.s3.connection import S3Connection
import sys

con = S3Connection('','')
dd=con.get_bucket('divvy_data')

while True:
    current_file_name=datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.json'
    if dd.get_key(current_file_name) == None:
        json_file = urllib.urlopen('http://www.divvybikes.com/stations/json')
        json_text=json_file.read()
        try: 
            current_state = json.loads('[' + json_text + ']')[0]
            key = dd.new_key(current_file_name)
            key.set_contents_from_string(current_state)
        except: 
            print 'error', sys.exc_info()[0]
    time.sleep(30)