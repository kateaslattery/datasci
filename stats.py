import pandas as pd
import scipy.stats as stats

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()

data = [i.split(', ') for i in data]

column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

stats_column_names = ["Mean", "Median", "Mode", "Range"]

df2 = pd.DataFrame(columns=stats_column_names) 

df2["Mean"] = [df['Alcohol'].mean(), df['Tobacco'].mean()]

df2["Median"] = [df['Alcohol'].median(), df['Tobacco'].median()] 

df2["Mode"] = [stats.mode(df['Alcohol']), stats.mode(df['Tobacco'])] # how to print this line?

df2["Range"] = [max(df['Alcohol']) - min(df['Alcohol']), max(df['Tobacco']) - min(df['Tobacco'])]

df2["Variance"] = [df['Alcohol'].var(), df['Tobacco'].var()]

df2["StdVar"] = [df['Alcohol'].std(), df['Tobacco'].std()]

print "The mean for the Alcohol dataset is: " 
print df2.iloc[0,0]
print " and the mean for the Tobacco dataset is: " 
print df2.iloc[1,0]  

print "The median for the Alcohol dataset is: " 
print df2.iloc[0,1]
print " and the median for the Tobacco dataset is: " 
print df2.iloc[1,1]  

print "The mode for the Alcohol dataset is: " 
print df2.iloc[0,2]
print " and the mode for the Tobacco dataset is: " 
print df2.iloc[1,2]  

print "The range for the Alcohol dataset is: " 
print df2.iloc[0,3]
print " and the range for the Tobacco dataset is: " 
print df2.iloc[1,3]  

print "The variance for the Alcohol dataset is: " 
print df2.iloc[0,4]
print " and the variance for the Tobacco dataset is: " 
print df2.iloc[1,4]  

print "The standard variation for the Alcohol dataset is: " 
print df2.iloc[0,5]
print " and the standard variation for the Tobacco dataset is: " 
print df2.iloc[1,5]  
