import urllib
import datetime
import os, time, socket, datetime, glob
import subprocess

socket.setdefaulttimeout(20)

def group_previous_days_files():
    print "Attempting grouping..."
    print "bozo..."
    todays_group = datetime.datetime.now().strftime('%Y%m%d')
    print "Today's group is " + todays_group
    log_filenames = [file_path for file_path in glob.glob("./DownloadedData/*.json") if not todays_group in file_path and not 'day_' in file_path]
    print "Logs found: " + str(log_filenames)
    for log_filename in log_filenames:
        print "Grouping " + log_filename
        base_log_filename = os.path.basename(log_filename)
        the_date = base_log_filename.split('_')[0]
        grouped_file_path = data_folder + 'day_' + the_date + '.json'
        with open(grouped_file_path, 'a') as day_file:
            with open(log_filename, 'r') as minute_file:
                minute_text = minute_file.read()
                day_file.write(minute_text)
        print "Removing " + log_filename
        os.remove(log_filename)
    #subprocess.call(['s3cmd', 'sync', './DownloadedData/day_*.json', 's3://bozo-divvy/day-log/'])
    os.system('s3cmd sync ./DownloadedData/day_*.json s3://bozo-divvy/day-log/')
    print "Done uploading to S3"
    for day_file in glob.glob('./DownloadedData/day_*.json'):
        os.remove(day_file)

data_folder = './DownloadedData/'
while True:
    current_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.json'
    current_file_path = data_folder + current_file_name
    if not os.path.exists(current_file_path):
        print "Downloading file... then sleeping."
        try:
            urllib.urlretrieve ("http://divvybikes.com/stations/json", current_file_path)
        except:
             time.sleep(3)
             continue
        group_previous_days_files()
    else:
        print "File already exists. Sleeping"
    time.sleep(30)
