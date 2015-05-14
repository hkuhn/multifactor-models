
from pandas import *
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt 
import statsmodels.api as sm

beginning_date = 196401
ending_date = 201201

# ESTIMATE BETAS
# retrieve data and select data from 1964 to 2011
monthly_returns = read_csv('../../data/3-fama-french-factor-model/mkt-smb-hml.csv')
beginning_index = monthly_returns[monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = monthly_returns[monthly_returns['Date'] == ending_date].index.tolist()
monthly_returns = monthly_returns[beginning_index[0]:ending_index[0]]

# remove date
monthly_returns = monthly_returns.ix[:,1:]

for index in monthly_returns.ix[:,1:].keys():
	X = transpose(array([monthly_returns["Rm- Rf"]]))
	y = monthly_returns[index]
	X = sm.add_constant(X)
	result = sm.OLS(y, X).fit()
	result.summary()

