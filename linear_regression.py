# Linear Regression
# A lesson in modelling linear relationships to describe the correlation of two variables to each other.
                          
import matplotlib.pyplot as plt                      #(simple data visualizations- histograms, scatter plots, box plot)
import pandas as pd                                  #(structures data into data frames)
import statsmodels.api as sm                         #(read from csv, analyze dataframes)   
import numpy as np                                   #(stats visualizations)
import math                                          #(computing package- matrix multiplication)
from sklearn.linear_model import LogisticRegression

# Import Data

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dtypes

# -----------
# Clean Data 
# -----------

# Strip %
StripSign = lambda element: round(float(element.rstrip('%'))/100, 4)

# Strip Unit
StripUnit = lambda element: int(element.rstrip(' months'))

# Convert to string, Split on '-'
SplitFico = lambda element: str(element).split('-')

# Convert pairs of FICO scores to int, pick min
ConvFico = lambda element: min([int(num) for num in element])


# Strip % from Interest Rate Column
loansData['Interest.Rate'] = map(StripSign, loansData['Interest.Rate'])

# Strip Month from loan length Column

loansData['Loan.Length'] = map(StripUnit, loansData['Loan.Length'])

# Split FICO scores on '-' and choose min of each pair
loansData['FICO.Score'] = map(SplitFico, loansData['FICO.Range'])
loansData['FICO.Score'] = map(ConvFico, loansData['FICO.Score'])

#print loansData['Interest.Rate'][0:5]
#print loansData['Loan.Length'][0:5]
#print loansData['FICO.Score'][0:5]

loansData.to_csv('loansData_clean.csv', header=True, index=False)

plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')

# Define a linear model

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
print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared

# -P-Value should be 0.05 or less
# - R is a "coefficient of correlation" between the independent variables and the dependent variable
# - A high R2 would be close to 1.0, and a low one close to 0
