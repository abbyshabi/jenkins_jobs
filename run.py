import jenkins
from jenkinsapi.jenkins import Jenkins
import sqlite3
import requests
import datetime

'''
The method init_server is for setting up and defining the required parameters
'''
def init_server(url, username, password):
    J = jenkins.Jenkins(url,username=username, password=password)
    return J

url = 'http://localhost:8080'
print('please enter your username')
username = raw_input()
print('please enter your password')
password = raw_input()
J = init_server(url, username, password)

'''
This is for validation and authentication 
'''
authenticated = False
if J.get_whoami() == username:
    authenticated = True
else:
    print("incorrect credentials")
    authenticated = False


'''
Initialization of the sqlite3 datatbase after successful authentication
'''
conn = sqlite3.connect('jenkins_jobs.db') 
c = conn.cursor()


'''
A loop is created to fetch data from Jenkinsapi
'''
for job,instance in server.get_all_jobs():

    '''
    Using an If statement to determine the status of Jobs and for Output
    '''
    if instance.get_last_good_build() == None :
         status = 'NOT_BUILT' #the get_last_good_build is a jenkins function 
    elif instance.is_running():
        status = 'SUCCESS'
    else:
        status = J.get_job(instance.name).get_last_build().get_status()
	    
    job_list = (instance.name, status,datetime.now())
    c.execute("SELECT id FROM jenkins_jobs WHERE job_name = ?", (instance.name,))
    data=c.fetchone()
    if data is None:
    	c.execute('INSERT INTO jenkins_jobs (job_name, status, date_checked) VALUES (?,?,?)', job_list)
    else:
    	update_list = (status, instance.name,datetime.now())
    	c.execute('UPDATE jenkins_jobs SET status=?, date_checked=? WHERE job_name=?', update_list)
		
'''
commit changes to the database
'''
conn.commit()

c.execute('SELECT * from jenkins_jobs')
jobs = c.fetchall()
for id, job, status in jobs:
	print(job)
	
'''
End database connection
''' 
conn.close()
	
