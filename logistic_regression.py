# Logistic Regression (built of the Linear Regression model)
# A lesson in modelling categorical variables to predict the likelihood of events occuring.
                            
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import sys

# Import Data

df = pd.read_csv('loansData_clean.csv')

# -----------
# Clean Data 
# -----------

# Determine if interest rate is < 12%
df['IR_TF'] = df['Interest.Rate'].map(lambda num: num < 0.12)

# Add intercept column 
df['Intercept'] = 1

# Create list of independent variables
ind_vars = ['FICO.Score', 'Amount.Requested', 'Intercept']

# -----------
# Logistic Regression Model 
# -----------

# Define the model using FICO Score and Amount Requested to predict if the Interest Rate will be < 12% 
logit = sm.Logit(df['IR_TF'], df[ind_vars])

# Fit the model
result = logit.fit()
coeff = result.params
#print coeff

# -----------
# Logistic Regression Prediction
# -----------

# Function takes a FICO Score and Loan Amount of the linear predictor and returns p. 
FicoScore = int(raw_input('FICO Score: '))
LoanAmount = int(raw_input('Loan Amount: '))

def logistic_function(FicoScore,LoanAmount,coeff):
	p = 1/(1 + np.exp(-(coeff[2] + coeff[0]*FicoScore + coeff[1]*LoanAmount)))
	return p
 
# Determine the value of p that shouls be used as a cutoff by visualizing the logistic function for loan amount $10000
x = np.arange(550,950,1)
y = 1/(1 + np.exp(-coeff[2] - coeff[0]*x - coeff[1]*10000))
plt.figure()
plt.plot(x,y)
plt.draw()
plt.savefig('logistic_function.png')


 # Prediction Function
def prediction(FicoScore,LoanAmount,coeff):
	p = logistic_function(FicoScore,LoanAmount,coeff)
	if p >= 0.70:
		print('You will get a loan with an interest rate under 12%')
	else:
		print('Sorry, you will not get a loan with an interest rate under 12%')
  
prediction(FicoScore,LoanAmount,coeff)
