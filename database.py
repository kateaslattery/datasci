# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:30:56 2015

@author: kslattery
"""

import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

with con:
  # From the connection, you get a cursor object. The cursor is what goes over the records that result from a query.
  cur = con.cursor()    
  cur.execute("DROP TABLE IF EXISTS cities")
  cur.execute("DROP TABLE IF EXISTS weather")
  cur.execute("CREATE TABLE cities (name text, state text)")
  cities = [
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA')
  ]
  cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
  cur.execute('CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)')
  weather = [
    ('New York City', 2013, 'July', 'January', 62),     
    ('Boston', 2013, 'July', 'January', 59),    
    ('Chicago', 2013, 'July', 'January', 59),     
    ('Miami', 2013, 'July', 'January', 84),     
    ('Dallas', 2013, 'July', 'January', 77),     
    ('Seattle', 2013, 'July', 'January', 61),     
    ('Portland', 2013, 'July', 'December', 63),     
    ('San Francisco', 2013, 'September', 'December', 64),     
    ('Los Angeles', 2013, 'September', 'December', 75)
    ]
  cur.executemany("INSERT INTO weather VALUES (?,?,?,?,?)", weather)
  cur.execute("SELECT name, state FROM cities INNER JOIN weather ON name = city GROUP BY warm_month = 'July'")
  rows = cur.fetchall()
  df = pd.DataFrame(rows)
  name = df[0]
  state = df[1]
  for row in rows:
      warmest = {0}, {1}.format(name, state)
  print "The cities that are warmest in July are:"
      
 
