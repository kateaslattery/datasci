import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Requested')
plt.savefig("Lending_Requested_Boxplot")

plt.figure()
loansData.hist(column='Amount.Requested')
plt.savefig("Lending_Requested_Histogram")

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig("Lending_Requested_QQ_Plot")

plt.figure()
loansData.boxplot(column='Amount.Funded.By.Investors')
plt.savefig("Lending_Funded_Boxplot")

plt.figure()
loansData.hist(column='Amount.Funded.By.Investors')
plt.savefig("Lending_Funded_Histogram")

plt.figure()
graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)
plt.savefig("Lending_Funded_QQ_Plot")
