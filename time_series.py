import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# -----------
# Import 2014 lending Club Statistics
# -----------

df = pd.read_csv('LoanStats3b.csv', header=1, low_memory=False)

# Converts string to datetime object in pandas:
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

df = df.dropna(subset=['issue_d'])

# set the dataframe index as monthly periods
index = pd.PeriodIndex(df.issue_d, freq='M')
df = df.set_index(index)

# group by to get the time series
issuedts = df['issue_d'].groupby(df.index).count()

# plot the issued loans time series
plt.figure()
issuedts.plot()
plt.ylabel('Issued Loans')
plt.draw()
plt.savefig('time_series_plot.png')

# plot the ACF of the time_series
plt.figure()
sm.graphics.tsa.plot_acf(issuedts)
plt.draw()
plt.savefig('acf_plot.png')

# plot the PACF of the time_series
plt.figure()
sm.graphics.tsa.plot_pacf(issuedts)
plt.draw()
plt.savefig('pacf_plot.png')

# compute a differenced set of the data because of the incompatabilitiy
# with the assumptions of an AR model
issueddiff = []
for i in range(len(issuedts) - 1):
	diff = issuedts[len(issuedts)-1-i] - issuedts[len(issuedts)-2-i]
	issueddiff = [diff] + issueddiff

issueddiff = pd.Series(issueddiff)

# plot the issued loans time series
plt.figure()
issueddiff.plot()
plt.ylabel('Differenced Issued Loans')
plt.draw()
plt.savefig('differenced_series_plot.png')

# plot the ACF of the time_series
plt.figure()
sm.graphics.tsa.plot_acf(issueddiff)
plt.draw()
plt.savefig('acf_plot_differenced.png')

# plot the PACF of the time_series
plt.figure()
sm.graphics.tsa.plot_pacf(issueddiff)
plt.draw()
plt.savefig('pacf_plot_differenced.png')

# show all plots
plt.show()
