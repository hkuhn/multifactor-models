
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
dp_monthly_returns = read_csv('../../data/3-fama-french-factor-model/d-p-monthly-data.csv')
mkt_monthly_returns = read_csv('../../data/3-fama-french-factor-model/mkt-smb-hml-rf.csv')
mkt_monthly_returns = mkt_monthly_returns[["Date", "Mkt-RF", "RF", "SMB", "HML"]]

beginning_index = dp_monthly_returns[dp_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = dp_monthly_returns[dp_monthly_returns['Date'] == ending_date].index.tolist()
dp_monthly_returns = dp_monthly_returns[beginning_index[0]:ending_index[0]]

beginning_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == ending_date].index.tolist()
mkt_monthly_returns = mkt_monthly_returns[beginning_index[0]:ending_index[0]]

# remove date
dp_monthly_returns = dp_monthly_returns.ix[:,1:]
mkt_monthly_returns = mkt_monthly_returns.ix[:,1:]
dp_monthly_returns = dp_monthly_returns.reset_index()
mkt_monthly_returns = mkt_monthly_returns.reset_index()

# subtract RF from DP returns
dp_keys = dp_monthly_returns.keys()
for index in dp_keys:
	dp_monthly_returns[index] = dp_monthly_returns[index].subtract(mkt_monthly_returns['RF'])

# combine return frames
dp_monthly_returns['Mkt-RF'] = mkt_monthly_returns['Mkt-RF']
dp_monthly_returns['RF'] = mkt_monthly_returns['RF']
dp_monthly_returns['SMB'] = mkt_monthly_returns['SMB']
dp_monthly_returns['HML'] = mkt_monthly_returns['HML']
monthly_returns = dp_monthly_returns

result_list = {}
for index in monthly_returns.ix[:,:-4].keys():
	X = transpose(array([monthly_returns["Mkt-RF"], monthly_returns["SMB"], monthly_returns["HML"]]))
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

