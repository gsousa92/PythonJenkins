import jenkins
import sqlite3
from sqlite3 import Error
import datetime
from datetime import datetime
import time
import cmd
import getpass

db_name = input('DB path(double slash on directories: ')
table_name = input('Table name: ')
url_jenkins = input('Url Jenkins: ')
user = input('User: ')
pw = getpass.getpass('Password: ')

server = jenkins.Jenkins(url_jenkins,
                         username=user, password=pw)
conn = sqlite3.connect(db_name)

jobs_number = len(server.get_jobs())
jobs_name = []
last_builds_number = []
jobs_last_build_status = []
timestamp = datetime.now()

for x in range(0, jobs_number):
    jobs_name.append(server.get_jobs()[x]['name'])
    last_builds_number.append(server.get_job_info(jobs_name[x])[
        'lastBuild']['number'])

for x in range(0, jobs_number):
    jobs_last_build_status.append(server.get_build_info(
        jobs_name[x], last_builds_number[x]))


c = conn.cursor()
try:
    c.execute("CREATE TABLE " + table_name +
          " (Class text, Id text, Name text, Description text, Status text,  Duration text, EstimatedDuration text, Url text, Timestamp text)")
    conn.commit()

except sqlite3.Error as e:
    print('Error creating Database: ', e)

try:    
    for x in range(0, jobs_number):
        c.execute("INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name),
                (jobs_last_build_status[x]['_class'],
                str(jobs_last_build_status[x]['id']),
                    jobs_last_build_status[x]['fullDisplayName'],
                    jobs_last_build_status[x]['description'],
                    jobs_last_build_status[x]['result'],
                    str(jobs_last_build_status[x]['duration']),
                    str(jobs_last_build_status[x]['estimatedDuration']),
                    jobs_last_build_status[x]['url'],
                    str(timestamp)))

    conn.commit()

except sqlite3.Error as e:
    print('Error Inserting Values: ', e)

conn.close()
