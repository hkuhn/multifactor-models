
from pandas import *
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt 
from scipy import stats
import statsmodels.api as sm

beginning_date = 196401
ending_date = 201201

# ESTIMATE BETAS
# retrieve data and select data from 1964 to 2011
dp_monthly_returns = read_csv('../../data/5-conditional-capm/d-p-monthly-data.csv')
mkt_monthly_returns = read_csv('../../data/5-conditional-capm/mkt-smb-hml-rf.csv')
mkt_monthly_returns = mkt_monthly_returns[["Date", "Mkt-RF", "RF"]]
macro_factors = read_csv('../../data/5-conditional-capm/macro-variables.csv')

beginning_index = dp_monthly_returns[dp_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = dp_monthly_returns[dp_monthly_returns['Date'] == ending_date].index.tolist()
dp_monthly_returns = dp_monthly_returns[beginning_index[0]:ending_index[0]]

beginning_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = mkt_monthly_returns[mkt_monthly_returns['Date'] == ending_date].index.tolist()
mkt_monthly_returns = mkt_monthly_returns[beginning_index[0]:ending_index[0]]

beginning_index = macro_factors[macro_factors['Date'] == beginning_date].index.tolist()
ending_index = macro_factors[macro_factors['Date'] == ending_date].index.tolist()
macro_factors = macro_factors[beginning_index[0]:ending_index[0]]


# index on date
dp_monthly_returns = dp_monthly_returns.ix[:,1:]
mkt_monthly_returns = mkt_monthly_returns.ix[:,1:]
macro_factors = macro_factors.ix[:,1:]
dp_monthly_returns = dp_monthly_returns.reset_index()
mkt_monthly_returns = mkt_monthly_returns.reset_index()
macro_factors = macro_factors.reset_index()

# subtract RF from DP returns
dp_keys = dp_monthly_returns.keys()
for index in dp_keys:
	dp_monthly_returns[index] = dp_monthly_returns[index].subtract(mkt_monthly_returns['RF'])

# combine return frames
dp_monthly_returns['Mkt-RF'] = mkt_monthly_returns['Mkt-RF']
dp_monthly_returns['RF'] = mkt_monthly_returns['RF']
monthly_returns = dp_monthly_returns

# run regression to obtain parameters on macro factors
# solve beta
#	alpha = const
#	gamma 0 = mkt - rf
#	gamma 1 = def * (mkt - rf)
#	gamma 2 = div * (mkt - rf)
#	gamma 3 = tb * (mkt - rf)
#	gamma 4 = term * (mkt - rf)
X_matrix = transpose(array([monthly_returns["Mkt-RF"], \
	macro_factors["def"].multiply(monthly_returns["Mkt-RF"]), \
	macro_factors["div"].multiply(monthly_returns["Mkt-RF"]), \
	macro_factors["Rf"].multiply(monthly_returns["Mkt-RF"]), \
	macro_factors["term"].multiply(monthly_returns["Mkt-RF"]) \
	]))

for index in monthly_returns.ix[:,:-2].keys():
	X = X_matrix
	y = monthly_returns[index]
	X = sm.add_constant(X)
	result = sm.OLS(y, X).fit()
	print result.summary()

