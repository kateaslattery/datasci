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

# ---------------
# Import Data
# ---------------

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
	cur.execute("DROP TABLE IF EXISTS undata")
	cur.execute("CREATE TABLE undata (country TEXT, year INT, men INT, women INT);")
	cur.executemany('INSERT INTO undata (country, year, men, women) VALUES (?, ?, ?, ?)', data_element)


# -------------
# Data analysis
# -------------

# Save data in dataframe
df = pd.DataFrame(data_element, columns=['Country','Year','Male Exp','Female Exp'])
df['Year'] = pd.PeriodIndex(df['Year'], freq='A-DEC')
df = df.set_index('Year', drop=False)
df[['Male Exp','Female Exp']] = df[['Male Exp','Female Exp']].astype(int)

print 'The mean school life expectancies are:'
print df[['Male Exp','Female Exp']].mean()
print 'The median expectacies are:'
print df[['Male Exp','Female Exp']].median()
print 'The variances are:'
print df[['Male Exp','Female Exp']].var()
print ' '

plt.figure()
df[['Male Exp','Female Exp']].hist()
plt.draw()
plt.savefig('histograms.png')

plt.figure()
df[['Male Exp','Female Exp']].boxplot()
plt.draw()
plt.savefig('boxplots.png')
