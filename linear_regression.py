# coding: utf-8

# Linear Regression
# 
# 
# A lesson in modelling linear relationships to describe the correlation of two variables to each other.
# 

# 1. Load Libraries

#get_ipython().magic(u'matplotlib inline')
                                   # (simple data visualizations- histograms, scatter plots, box plot)
import matplotlib.pyplot as plt    # (structures data into data frames)
import pandas as pd                # (read from csv, analyze dataframes)
import statsmodels.api as sm       # (stats visualizations)
import numpy as np                 # (computing package- matrix multiplication)


# 2. Explore Data

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dtypes

loansData['Interest.Rate'][0:5]


loansData['Loan.Length'][0:5]


loansData['FICO.Range'][0:5]


# 3. Clean Data
#    To convert data into a raw, homogenous format the units must be removed. Specifically, the "%" on the Interest Rates, the "months" on the Loan Lenghts and the range for the FICO ranges.
#    Lambda functions will be used to avoid binding the function to a name. 

loansData['Interest.Rate'] = map(lambda x: x.rstrip("%"),(loansData["Interest.Rate"]))
loansData['Interest.Rate'][0:5]


loansData['Loan.Length'] = map(lambda x: x.rstrip(" months"), loansData['Loan.Length'])
loansData['Loan.Length'][0:5]


#cleanFicoRange = map(lambda x: x.split('-'), loansData['FICO.Range'])
#loansData['FICO.Score'] = cleanFicoRange
#loansData['FICO.Range'] = loansData['FICO.Score'] #how to select just first column?
#loansData['FICO.Range'][0:5]

loansData['FICO.Score'] = [float(val.split('-')[0]) for val in loansData['FICO.Range']]
loansData['FICO.Score'][0:5]


# 3. Plot the data


plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()


a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')


# 4. Define a linear model

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']
# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()
# Create an input matrix
x = np.column_stack([x1,x2])
# Create a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
# Output the results
f.summary()


# - p-value should be 0.05 or less
# - R is a "coefficient of correlation" between the independent variables and the dependent variable
# - A high R2 would be close to 1.0, and a low one close to 0
