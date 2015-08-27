# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 17:04:31 2015

@author: kslattery
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns
# ---------------------------------
# Import school life expectacy data
# ---------------------------------

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)

#search for total school expectancy (in years) for each country
data = soup('table')[6].find_all('tr')
data = data[3]
data = data('table')[0]
data = data('tr')
#print data

# store html as tuples
data_element = []
for i in range(4, len(data)):
    tags = data[i]
    values = [tag.string for tag in tags('td')]
    data_element.append(list(values[i] for i in [0, 1, 7, 10]))
data_element = [tuple(element) for element in data_element]
#print data_element


# --------------------------
# Store data in SQlite table
# --------------------------

con = lite.connect('education.db')
cur = con.cursor()

with con:
	cur.execute("DROP TABLE IF EXISTS ed_data")
	cur.execute("CREATE TABLE ed_data (country TEXT, year INT, men INT, women INT);")
	cur.executemany('INSERT INTO ed_data (country, year, men, women) VALUES (?, ?, ?, ?)', data_element)


# -------------
# Data analysis
# -------------

# Save data in dataframe
df = pd.DataFrame(data_element, columns=['country','year','men','women'])
df['year'] = pd.PeriodIndex(df['year'], freq='A-DEC')
df = df.set_index('year', drop=False)
df[['men','women']] = df[['men','women']].astype(int)

print ' '
print 'For the men, and women school life expectancies'
print 'The means are:'
print df[['men','women']].mean()
print 'The medians are:'
print df[['men','women']].median()
print 'and the variances are:'
print df[['men','women']].var()
print ' '

plt.figure()
df[['men','women']].hist()
plt.draw()
plt.savefig('histograms.png')

plt.figure()
df[['men','women']].boxplot()
plt.draw()
plt.savefig('boxplots.png')

# -------------
# Import GDP data
# -------------

df = pd.read_csv('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv')

# save columns of interest 
gdp_data = pd.period_range('1999', '2010', freq='A-DEC')
gdp_data = list(str(periodval) for periodval in gdp_data)
columns_subset = ['Country Name'] + gdp_data
df = df[columns_subset]

with con:
	# clear table if it exists
	cur.execute("DROP TABLE IF EXISTS gdp_data")
	# create maxtemps table
	cur.execute("CREATE TABLE gdp_data (country TEXT, year INT, gdp NUMERIC);")
	#loop over countries and years
	for dfidx in df.index: 
		fillvalues = []
		for year in gdp_data:
			fillvalues = fillvalues + [(df.ix[dfidx]['Country Name'], year, df.ix[dfidx][year])]
			# fill dates
		cur.executemany('INSERT INTO gdpdata (country, year, gdp) VALUES (?, ?, ?)', fillvalues)

# Save into a dataframe
query = ("SELECT t1.country, t1.year, men, women, gdp "
	     "FROM ed_data t1 "
	     "INNER JOIN gdp_data t2 ON t1.country=t2.country "
	     "AND t1.year=t2.year")
df = pd.read_sql_query(query, con)

df.dropna(inplace=True)
