# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:04:20 2015

@author: kslattery
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

# -----------
# Import 2014 lending Club Statistics
# -----------

df = pd.read_csv('LoanStats3c.csv', index_col=0, low_memory=False)
#print df.dtypes

# -----------
# Clean Data
# -----------

# Remove Nulls
df.dropna(subset=['issue_d'], inplace=True)

# Strip %

StripSign = lambda element: round(float(element.rstrip('%'))/100, 4)

# Convert to integers
toInt = lambda element: int(element)


# Strip % from Interest Rate Column
df['int_rate'] = map(StripSign, df['int_rate'])

# Convert incomes to integers
df['annual_inc'] = map(toInt, df['annual_inc'])

# Transform annual income via log, base 10 
df['annual_inc_log'] = df['annual_inc'].map(lambda num: np.log10(num))

# -----------
# Model Interest Rates based off Annual Income
# -----------

IntRate = df['int_rate']
AnnualIncomeLog = df['annual_inc_log']

y = np.matrix(IntRate).transpose() # Response
x = np.matrix(AnnualIncomeLog).transpose() # Predictor
X = sm.add_constant(x)  # Adds a constant term to the predictor

est = sm.OLS(y,X).fit()
print est.summary()
print est.params

logsample = np.arange(min(df['annual_inc_log']), max(df['annual_inc_log']), 0.1)
plt.figure()
plt.scatter(df['annual_inc_log'],df['int_rate'], alpha=0.3)
plt.xlabel('Log of Annual Income')
plt.ylabel('Interest Rate')
plt.plot(est.params[0] + est.params[1]*logsample, 'r')
plt.draw()

plt.savefig('InterestRate_vs_AnnualIncome.png')

# -----------
# Addition of Home Ownership variable
# -----------

df['homeOwner'] = pd.Categorical(df.home_ownership).labels

# Multiple regression model
est2 = smf.ols(formula="int_rate ~ homeOwner*annual_inc_log", data=df).fit()
print est2.summary()

'''
y = df.int_rate  # response
X = df.annual_inc_log  # predictor
X = sm.add_constant(X)  # Adds a constant term to the predictor
print X.head()

est = sm.OLS(y, X)

est = est.fit()
est.summary()

est.params

# We pick 100 hundred points equally spaced from the min to the max
X_prime = np.linspace(X.annual_inc_log.min(), X.annual_inc_log.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

# Now we calculate the predicted values
y_hat = est.predict(X_prime)

plt.scatter(X.annual_inc_log, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Annual Income")
plt.ylabel("Interest Rate")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red

# formula: response ~ predictors
est = smf.ols(formula='int_rate ~ annual_inc_log', data=df).fit()
est.summary()

# Fit the no-intercept model
est_no_int = smf.ols(formula='int_rate ~ annual_inc_log - 1', data=df).fit()

# We pick 100 hundred points equally spaced from the min to the max
X_prime_1 = pd.DataFrame({'annual_inc_log': np.linspace(X.annual_inc_log.min(), X.annual_inc_log.max(), 100)})
X_prime_1 = sm.add_constant(X_prime_1)  # add constant as we did before

y_hat_int = est.predict(X_prime_1)
y_hat_no_int = est_no_int.predict(X_prime_1)

fig = plt.figure(figsize=(8,4))
splt = plt.subplot(121)

splt.scatter(X.annual_inc_log, y, alpha=0.3)  # Plot the raw data
#plt.ylim(30, 100)  # Set the y-axis to be the same
plt.xlabel("Annual Income")
plt.ylabel("Interest Rate")
plt.title("With intercept")
splt.plot(X_prime[:, 1], y_hat_int, 'r', alpha=0.9)  # Add the regression line, colored in red

splt = plt.subplot(122)
splt.scatter(X.annual_inc_log, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Annual Income")
plt.title("Without Intercept")
splt.plot(X_prime[:, 1], y_hat_no_int, 'r', alpha=0.9)  # Add the regression line, colored in red

'''
