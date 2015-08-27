# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 21:52:29 2015

@author: kslattery

Acquiring Weather Data from an API

Collect the max temperatures in 5 major US cities over the course of a month. 
Determine which city has the largest temperature swings.

API: forecast.io- powers the Dark Sky mobile app.

"""
import sqlite3 as lite
import datetime
import requests
import pandas as pd
import collections

# ---------------
# API Information
# ---------------

cities = { "LA": '34.019394,-118.410825',
            "Miami": '25.775163,-80.208615',
            "NewOrleans": '30.053420,-89.934502',
            "NYC": '40.663619,-73.938589',
            "DC": '38.904103,-77.017229'

        }
        
end_date = datetime.datetime.now() 


api_key = '542da3a6578eb734d6985bbd9c6f6e9c'
url = 'https://api.forecast.io/forecast/' + api_key + '/'

# ---------------
# API Connection
# ---------------

# Establish database connection
con = lite.connect('weather.db')
cur = con.cursor()

cities.keys()
with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, LA REAL, Miami REAL, NewOrleans REAL, NYC REAL, DC REAL);') #New database table: daily_temp

query_date = end_date - datetime.timedelta(days=30) #the current value being processed

#create date column in daily_temp
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)

#add daily temperature max column to daily_temp table for the previous 30 days
for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day

# transfer the weather data from daily_temp into a dataframe
df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading", con)

# convert the dates to datetime objects for indexing
pd.to_datetime(df['day_of_reading'], unit='s')
df.set_index('day_of_reading', drop=True, inplace=True)


# --------------------
# Analysis: Greatest Temp Change
# --------------------

# Total temp change per city

tot_change = collections.defaultdict(int)

for column in df.columns:
	
	city_temps = df[column].tolist()
	
	temp_change = 0;
 
	for i in range(len(city_temps)-1):
		temp_change += abs(city_temps[i] - city_temps[i+1])
		tot_change[column] = temp_change

# find the station with the max activity
max_temp_range = max(tot_change, key=tot_change.get)

print "The city with the highest change in max temps is: " + max_temp_range
print "with an aggregate change in temperature of: " + str(tot_change[max_temp_range]) + " degrees over the past 30 days."


# -------------------
# Analysis: Greatest temp swing
# -------------------

swing = collections.defaultdict(int)

for column in df.columns:
	
	city_temps = df[column].tolist()
	
	swing[column] = 0
	for i in range(len(city_temps)-1):
		tempchange = abs(city_temps[i] - city_temps[i+1])
		if swing[column] < tempchange:
			swing[column] = tempchange

# find the station with the max activity
max_swing = max(swing, key=swing.get)

print "The city with the largest day-to-day temperature swing was: " + max_swing
print "with an day-to-day swing of: " + str(swing[max_swing]) + " degrees."

con.close() # a good practice to close connection to database
