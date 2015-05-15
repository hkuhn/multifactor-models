
from pandas import *
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt 
import statsmodels.api as sm

beginning_date = 196401
ending_date = 201201


# retrieve data and select data from 1964 to 2011
monthly_returns = read_csv('../../data/5-conditional-capm/mkt-smb-hml.csv')
beginning_index = monthly_returns[monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = monthly_returns[monthly_returns['Date'] == ending_date].index.tolist()
monthly_returns = monthly_returns[beginning_index[0]:ending_index[0]]

macro_factors = read_csv('../../data/5-conditional-capm/macro-variables.csv')
beginning_index = macro_factors[macro_factors['Date'] == beginning_date].index.tolist()
ending_index = macro_factors[macro_factors['Date'] == ending_date].index.tolist()
macro_factors = macro_factors[beginning_index[0]:ending_index[0]]

# remove date
monthly_returns = monthly_returns.ix[:,1:]
monthly_returns = monthly_returns.reset_index()
macro_factors = macro_factors.ix[:,1:]
macro_factors = macro_factors.reset_index()

# run regression to obtain parameters on macro factors
# solve beta
#	alpha = const
#	gamma 0 = mkt - rf
#	gamma 1 = def * (mkt - rf)
#	gamma 2 = div * (mkt - rf)
#	gamma 3 = tb * (mkt - rf)
#	gamma 4 = term * (mkt - rf)
X_matrix = transpose(array([monthly_returns["Rm- Rf"], \
	macro_factors["def"].multiply(monthly_returns["Rm- Rf"]), \
	macro_factors["div"].multiply(monthly_returns["Rm- Rf"]), \
	macro_factors["Rf"].multiply(monthly_returns["Rm- Rf"]), \
	macro_factors["term"].multiply(monthly_returns["Rm- Rf"]) \
	]))
for index in monthly_returns.ix[:,1:].keys():
	X = X_matrix
	y = monthly_returns[index]
	X = sm.add_constant(X)
	result = sm.OLS(y, X).fit()
	print result.summary()


# # PLOTTING
# plotting_data = monthly_returns.loc[:,['SMB', 'HML', 'Rm- Rf']]
# plotting_data["Rm- Rf"]
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter(plotting_data["Rm- Rf"], plotting_data["HML"], c='b', marker='s', label="HML")
# ax1.scatter(plotting_data["Rm- Rf"], plotting_data["SMB"], c='r', marker='o', label="SMB")
# #plotting_data.plot(x="Rm- Rf", y="HML", kind="scatter")
# line_plot = linspace(-20,20,600)
# ax1.plot(line_plot, line_plot*betas["SMB"] + alphas["SMB"], c='r')
# #plotting_data.plot(x="Rm- Rf", y="SMB", kind="scatter")
# another_line_plot = linspace(-20,20,600)
# ax1.plot(another_line_plot, another_line_plot*betas["HML"] + alphas["HML"], c='b')
# plt.legend(loc='upper left')
# plt.show()