
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
dp_monthly_returns = read_csv('../../data/3-fama-french-factor-model/d-p-monthly-data.csv')
mkt_monthly_returns = read_csv('../../data/3-fama-french-factor-model/mkt-smb-hml-rf.csv')
mkt_monthly_returns = mkt_monthly_returns[["Date", "Mkt-RF", "RF"]]

beginning_index = dp_monthly_returns[dp_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = dp_monthly_returns[dp_monthly_returns['Date'] == ending_date].index.tolist()

dp_monthly_returns = dp_monthly_returns[beginning_index[0]:ending_index[0]]
mkt_monthly_returns = mkt_monthly_returns[beginning_index[0]:ending_index[0]]

# remove date
dp_monthly_returns = dp_monthly_returns.ix[:,1:]
mkt_monthly_returns = mkt_monthly_returns.ix[:,1:]

# subtract RF from DP returns
dp_keys = dp_monthly_returns.keys()
for index in dp_keys:
	dp_monthly_returns[index] = dp_monthly_returns[index].subtract(mkt_monthly_returns['RF'])

# combine return frames
dp_monthly_returns['Mkt-RF'] = mkt_monthly_returns['Mkt-RF']
dp_monthly_returns['RF'] = mkt_monthly_returns['RF']
monthly_returns = dp_monthly_returns


# get estimations of parameters
means = monthly_returns.mean()
covariance_matrix = monthly_returns.cov()

betas = covariance_matrix['Mkt-RF'] / covariance_matrix['Mkt-RF']['Mkt-RF']
alphas = means - betas * means['Mkt-RF']

# get error terms by checking predictions with actual
alpha_ones = ones((1, len(monthly_returns.index)))
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)
betas_matrix = betas.as_matrix().reshape(len(betas.index), 1)
Rm = monthly_returns['Mkt-RF'].as_matrix().reshape(1, len(monthly_returns.index))

# the model
predicted_returns_matrix = multiply(alphas_matrix, alpha_ones) + betas_matrix * Rm
predicted_returns_matrix = predicted_returns_matrix.transpose()
predicted_returns = DataFrame(data=predicted_returns_matrix, index=monthly_returns.index, columns=monthly_returns.columns)

epsilons = monthly_returns.subtract(predicted_returns).mean()




# remove benchmarks
betas = betas.ix[:-2]
alphas = alphas.ix[:-2]
epsilons = epsilons.ix[:-2]

print "TRAINING A SHARPE FACTOR MODEL COMPLETE: "
print "Parameters Learned: "
print "\n\n\n\n"
print "Alphas: "
print DataFrame(data=[alphas], index=["alphas"], columns=alphas.index)
print "\n\n\n\n"
print "Betas: "
print DataFrame(data=[betas], index=["betas"], columns=betas.index)
print "Epsilons: "
print DataFrame(data=[epsilons], index=["epsilons"], columns=epsilons.index)
print "\n\n\n\n"

# TESTING PHASE
#	Testing if the beta factor are priced in the cross-section
#	Use the beta trained to estimate return on test data
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)
betas_matrix = betas.as_matrix().reshape(len(betas.index), 1)
epsilons_matrix = epsilons.as_matrix().reshape(len(epsilons.index), 1)

Rm_testing = monthly_returns['Mkt-RF'].as_matrix().reshape(1, len(monthly_returns.index))
monthly_returns = monthly_returns.ix[:,:-2]
testing_ones = ones((1, len(monthly_returns.index)))
testing_predicted_returns_matrix = multiply(alphas_matrix, testing_ones) + betas_matrix * Rm_testing + multiply(epsilons_matrix, testing_ones)
testing_predicted_returns_matrix = testing_predicted_returns_matrix.transpose()
testing_predicted_returns = DataFrame(data=testing_predicted_returns_matrix, index=monthly_returns.index, columns=monthly_returns.columns)
differences = monthly_returns.subtract(testing_predicted_returns)
difference_between_mean = monthly_returns.subtract(monthly_returns.mean())

# mean squared error
ss_res = (differences ** 2).sum()
ss_tot = (difference_between_mean ** 2).sum()
r_squared = 1.0 - (ss_res / ss_tot)
mse_data = ss_res / (len(monthly_returns.index))
t_stat_alpha = (alphas - 0.0) / alphas.sem()
t_stat_beta = (betas - 0.0) / betas.sem()

print "TESTING RESULTS: "
print "R squared: "
print DataFrame(data=[r_squared], index=["r squared"], columns=r_squared.index)
print "\n\n\n\n"
print "MSE: "
print DataFrame(data=[mse_data], index=["MSE"], columns=mse_data.index)
print "\n\n\n\n"
print "T Statistic for Alpha: (null=0)"
print t_stat_alpha
print "T Statistic for Beta: (null=0)"
print t_stat_beta
print "\n\n\n\n"



