import statsmodels.api as sm
import statsmodels.stats.api as diag
from patsy import dmatrices
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

all_data = pd.read_csv('projects/referendum votes/Worked data/all_data', index_col='Borough')

y, X = dmatrices("Q('Leave votes') ~ Q('Other Party') + Q('Labour Party') + Q('Green Party') + Q('UK Independence Party (UKIP)') + Q('Fear Crime') + Q('2015 Pay') + Q('% Turnout') + Q('Mixed') + Asian + Black + Q('Chinese/ Other')", data=all_data, return_type='dataframe')

results = sm.OLS(y, X).fit()

print results.summary()

fig,ax = plt.subplots(figsize=(15,12))

ax.plot(np.arange(30), y)

ax.plot(np.arange(30), results.fittedvalues)

fig.show()

fig,ax = plt.subplots(figsize=(15,12))

sorted_residuals = results.resid.sort_values()

fit = stats.norm.pdf(sorted_residuals, np.mean(sorted_residuals), np.std(sorted_residuals))

ax.plot(sorted_residuals,fit,'-o')

ax.hist(results.resid, normed=True)

fig.show()

'''Q-Q plot of residuals, test residuals lags if correlated'''

z = ((results.resid-np.mean(results.resid))/np.std(results.resid))

stats.probplot(z, dist='norm', plot=plt)

plt.show()

