# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:44:48 2015

@author: kslattery
"""
import requests
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np
import sqlite3 as lite
import time
from dateutil.parser import parse 
import collections

# -----------
# Import Data 
# -----------

r = requests.get('http://www.citibikenyc.com/stations/json')

print r.json().keys()

key_list = [] #unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)
            
from pandas.io.json import json_normalize

df = json_normalize(r.json()['stationBeanList'])

# -----------
# Analyze/Clean Data 
# -----------

#df['availableBikes'].hist()
#plt.show()

#df['totalDocks'].hist()
#plt.show()

#print df.availableBikes.mean()
#print df.availableBikes.median()

#print sum(df.testStation)

df['inService'] = df['statusValue'].map(lambda i: i == 'In Service')

#print sum(df.inService)

bikesInService = []
for i,j in zip(df.inService, df.availableBikes):
    if i == True:
        bikesInService.append(j)

#print np.mean(bikesInService)

condition = (df['statusValue'] == 'In Service')
#print df[condition]['totalDocks'].mean()

# -----------
# Store Data in SQLite 
# -----------

con = lite.connect('citi_bike.db')
cur = con.cursor()

# clear tables if they exist
with con:
	# clear tables if they exist
	cur.execute("DROP TABLE IF EXISTS citibike_reference")
	cur.execute("DROP TABLE IF EXISTS available_bikes")

with con: 
    sql = ("CREATE TABLE citibike_reference (id INT PRIMARY KEY, " 
    	"totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, "
    	"longitude NUMERIC, postalCode TEXT, testStation TEXT, "
    	"stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, "
    	"location TEXT )")
    cur.execute(sql)

#a prepared SQL statement we're going to execute over and over again
sql = ("INSERT INTO citibike_reference (id, totalDocks, "
    	"city, altitude, stAddress2, longitude, postalCode, "
    	"testStation, stAddress1, stationName, landMark, "
    	"latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")

#for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, 
        #stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],
                            station['stAddress2'],station['longitude'],station['postalCode'],
                            station['testStation'],station['stAddress1'],station['stationName'],
                            station['landMark'],station['latitude'],station['location']))
                            
#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids] 

#create the table
#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")
    
# ------------------
# STORE DYNAMIC DATA
# ------------------

# collect available bike data for one hour
for i in range(60):

    #take the execution time string and parse into a datetime object
	exec_time = parse(r.json()['executionTime'])

	# create entry for the execution time
	with con:
		sql = 'INSERT INTO available_bikes (execution_time) VALUES (?)'
		cur.execute(sql, (exec_time.strftime('%s'),))

	#defaultdict to store available bikes by station
	id_bikes = collections.defaultdict(int) 

	#loop through the stations in the station list
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	#iterate through the defaultdict to update the values in the database
	with con:
		for k, v in id_bikes.iteritems():
			sql = ("UPDATE available_bikes SET _" + str(k) + 
				   " = " + str(v) + " WHERE execution_time = " + 
				   exec_time.strftime('%s') + ";")
			cur.execute(sql)

	# wait sixty seconds
	time.sleep(60)

	# get new data
	r = requests.get('http://www.citibikenyc.com/stations/json')
