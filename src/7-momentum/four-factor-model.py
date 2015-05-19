
from pandas import *
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt 
from scipy import stats
import statsmodels.api as sm
from mpl_toolkits.mplot3d import Axes3D

beginning_date = 196401
ending_date = 201201

# ESTIMATE BETAS
# retrieve data and select data from 1964 to 2011
industry_monthly_returns = read_csv('../../data/7-momentum/sector_returns.csv')
mkt_monthly_returns = read_csv('../../data/7-momentum/mkt-smb-hml-rf.csv')
momentum = read_csv('../../data/7-momentum/mom.csv')
mkt_monthly_returns = mkt_monthly_returns[["Date", "Mkt-RF", "RF", "SMB", "HML"]]
mkt_monthly_returns["Mom"] = momentum["Mom"]

beginning_index = industry_monthly_returns[industry_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = industry_monthly_returns[industry_monthly_returns['Date'] == ending_date].index.tolist()
industry_monthly_returns = industry_monthly_returns[beginning_index[0]:ending_index[0]]

beginning_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == ending_date].index.tolist()
mkt_monthly_returns = mkt_monthly_returns[beginning_index[0]:ending_index[0]]

# remove date
industry_monthly_returns = industry_monthly_returns.ix[:,1:]
mkt_monthly_returns = mkt_monthly_returns.ix[:,1:]
industry_monthly_returns = industry_monthly_returns.reset_index()
mkt_monthly_returns = mkt_monthly_returns.reset_index()

# subtract RF from DP returns
keys = industry_monthly_returns.keys()
for index in keys:
	industry_monthly_returns[index] = industry_monthly_returns[index].subtract(mkt_monthly_returns['RF'])

# combine return frames
industry_monthly_returns['Mkt-RF'] = mkt_monthly_returns['Mkt-RF']
industry_monthly_returns['RF'] = mkt_monthly_returns['RF']
industry_monthly_returns['SMB'] = mkt_monthly_returns['SMB']
industry_monthly_returns['HML'] = mkt_monthly_returns['HML']
industry_monthly_returns['Mom'] = mkt_monthly_returns['Mom']
monthly_returns = industry_monthly_returns

result_list = {}
for index in monthly_returns.ix[:,:-5].keys():
	X = transpose(array([monthly_returns["Mkt-RF"], monthly_returns["SMB"], monthly_returns["HML"], monthly_returns["Mom"]]))
	y = monthly_returns[index]
	X = sm.add_constant(X)
	result = sm.OLS(y, X).fit()
	print result.summary()
	result_list[index] = result


#plotting_data = dp_monthly_returns.loc[:,['Dec 2', 'Mkt-RF', 'SMB']]
#plt.figure()
#plotting_data.plot(x="Mkt-RF", y="Dec 2", z="SMB", kind="scatter", title="Beta Regression on Dec 2")
#line_plot = linspace(-20,20,400)
#plt.plot(line_plot, line_plot*result_list["Dec 2"].params[1] + result_list["Dec 2"].params[0])
#plt.show()
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(monthly_returns["SMB"], monthly_returns["Mkt-RF"], monthly_returns["Dec 2"])

plt.show()

