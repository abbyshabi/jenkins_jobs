from jenkinsapi.jenkins import Jenkins
import jenkins
import sqlite3
import requests
from datetime import datetime


'''
Initialization of the sqlite3 datatbase 
'''
conn = sqlite3.connect('jenkins_jobs.db') 
cursor = conn.cursor()


'''
This method initializes the Jenkins connection using the required parameters
'''
def init_server(url, username, password):
    jenkins_server = Jenkins(url, username, password)
    return jenkins_server


url = 'http://localhost:8080'
username='dammy'
password='ambition1'

jenkins_server = init_server(url, username, password)

'''
Loop fetching data from Jenkinsapi using the .get_jobs() method
'''
for job, instance in jenkins_server.get_jobs():

    
    job_status = jenkins_server.get_job(instance.name).get_last_build().get_status()

    job_list = (instance.name, job_status, datetime.now())

    cursor.execute("SELECT id FROM jenkins_jobs WHERE job_name = ?", (instance.name,))
    data=cursor.fetchone()

    if data is None:
    	cursor.execute('INSERT INTO jenkins_jobs (job_name, job_status, job_date_checked) VALUES (?,?,?)', job_list)
    else:
    	update_list = (job_status, instance.name,datetime.now())
    	cursor.execute('UPDATE jenkins_jobs SET job_status=?, job_date_checked=? WHERE job_name=?', update_list)
		

'''
commit changes to the database
'''
conn.commit()

'''
Querying the database to display all jobs stored in it
'''
cursor.execute('SELECT * from jenkins_jobs')
jobs = cursor.fetchall()
for id, jobname, job_status, datechecked in jobs:
	print(jobname+' || '+job_status+' || '+datechecked)

'''
End database connection
''' 
conn.close()
	