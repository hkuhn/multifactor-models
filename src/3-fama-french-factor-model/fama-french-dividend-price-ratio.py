
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
mkt_monthly_returns = mkt_monthly_returns[["Date", "Mkt-RF", "RF", "SMB", "HML"]]

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
dp_monthly_returns['SMB'] = mkt_monthly_returns['SMB']
dp_monthly_returns['HML'] = mkt_monthly_returns['HML']
monthly_returns = dp_monthly_returns


# get estimations of parameters
means = monthly_returns.mean()
covariance_matrix = monthly_returns.cov()

market_betas = covariance_matrix['Mkt-RF'] / covariance_matrix['Mkt-RF']['Mkt-RF']
smb_betas = covariance_matrix['SMB'] / covariance_matrix['SMB']['SMB']
hml_betas = covariance_matrix['HML'] / covariance_matrix['HML']['HML']

alphas = means - market_betas * means['Mkt-RF'] - smb_betas * means["SMB"] - hml_betas * means["HML"]

# remove benchmarks
market_betas = market_betas.ix[:-4]
smb_betas = smb_betas.ix[:-4]
hml_betas = hml_betas.ix[:-4]
alphas = alphas.ix[:-4]

print "TRAINING A FACTOR MODEL COMPLETE: "
print "Parameters Learned: "
print "\n\n\n\n"
print "Market Betas: "
print DataFrame(data=[market_betas], index=["betas"], columns=market_betas.index)
print "SMB Betas: "
print DataFrame(data=[smb_betas], index=["betas"], columns=smb_betas.index)
print "HML Betas: "
print DataFrame(data=[hml_betas], index=["betas"], columns=hml_betas.index)
print "Alphas: "
print DataFrame(data=[alphas], index=["alphas"], columns=alphas.index)
print "\n\n\n\n"

# TESTING PHASE
#	Testing if the beta factor are priced in the cross-section
#	Use the beta trained to estimate return on test data
market_betas_matrix = market_betas.as_matrix().reshape(len(market_betas.index), 1)
smb_betas_matrix = smb_betas.as_matrix().reshape(len(smb_betas.index), 1)
hml_betas_matrix = hml_betas.as_matrix().reshape(len(hml_betas.index), 1)
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)


Rm_testing = monthly_returns['Mkt-RF'].as_matrix().reshape(1, len(monthly_returns.index))
SMB_testing = monthly_returns['SMB'].as_matrix().reshape(1, len(monthly_returns.index))
HML_testing = monthly_returns['HML'].as_matrix().reshape(1, len(monthly_returns.index))
Rf_testing = monthly_returns['RF'].as_matrix().reshape(1, len(monthly_returns.index))
monthly_returns = monthly_returns.ix[:,:-4]

testing_ones = ones((1, len(monthly_returns.index)))
testing_predicted_returns_matrix = Rf_testing +multiply(alphas_matrix, testing_ones) + market_betas_matrix * Rm_testing + smb_betas_matrix * SMB_testing + hml_betas_matrix * HML_testing
testing_predicted_returns_matrix = testing_predicted_returns_matrix.transpose()
testing_predicted_returns = DataFrame(data=testing_predicted_returns_matrix, index=monthly_returns.index, columns=monthly_returns.columns)
differences = monthly_returns.subtract(testing_predicted_returns)
difference_between_mean = monthly_returns.subtract(monthly_returns.mean())

# mean squared error
ss_res = (differences ** 2).sum()
ss_tot = (difference_between_mean ** 2).sum()
r_squared = 1.0 - (ss_res / ss_tot)
mse_data = ss_res / (len(monthly_returns.index))


print "TESTING RESULTS: "
print "R squared: "
print DataFrame(data=[r_squared], index=["r squared"], columns=r_squared.index)
print "\n\n\n\n"
print "MSE: "
print DataFrame(data=[mse_data], index=["MSE"], columns=mse_data.index)
print "\n\n\n\n"

monthly_returns = monthly_returns.iloc[:,:-4]
market_betas = market_betas.ix[:-4]
smb_betas = smb_betas.ix[:-4]
hml_betas = hml_betas.ix[:-4]

market_betas_array = market_betas.as_matrix()
smb_betas_array = smb_betas.as_matrix()
hml_betas_array = hml_betas.as_matrix()

gamma_0 = []
gamma_M = []
gamma_SMB = []
gamma_HML = []
for row in monthly_returns.iterrows():
	cross_section_returns_array = row[1].as_matrix()
	X = transpose(array([market_betas_array, smb_betas_array, hml_betas_array]))
	X = sm.add_constant(X)
	model = sm.OLS(cross_section_returns_array, X)
	model = model.fit()
	gamma_0.append(model.params[0])
	gamma_M.append(model.params[1])
	gamma_SMB.append(model.params[2])
	gamma_HML.append(model.params[3])


# retrieve average gammas
gamma_0_array = array(gamma_0)
gamma_M_array = array(gamma_M)
gamma_SMB_array = array(gamma_SMB)
gamma_HML_array = array(gamma_HML)
average_gamma_0 = average(gamma_0_array)
average_gamma_M = average(gamma_M_array)
average_gamma_SMB = average(gamma_SMB_array)
average_gamma_HML = average(gamma_HML_array)

std_err_mean_0 = std(gamma_0_array) / sqrt(len(gamma_0))
std_err_mean_M = std(gamma_M_array) / sqrt(len(gamma_M))
std_err_mean_SMB = std(gamma_SMB_array) / sqrt(len(gamma_SMB))
std_err_mean_HML = std(gamma_HML_array) / sqrt(len(gamma_HML))

# T-Statistic Population Parameters
#	M should equal the market excess return
#	0 should equal the risk free rate
t_stat_0, prob_0 = stats.ttest_1samp(gamma_0_array, means["RF"])
t_stat_M, prob_M = stats.ttest_1samp(gamma_M_array, means['Mkt-RF'])

print "Cross Section Regression on Returns of D/P Portfolios"
print "GAMMA 0: "
print average_gamma_0
print "GAMMA M: "
print average_gamma_M
print "\n"
print "STD ERR 0: "
print std_err_mean_0
print "STD ERR M: "
print std_err_mean_M
print "T STATISTIC 0: "
print t_stat_0
print "T STATISTIC M: "
print t_stat_M
print "P VALUE 0: "
print prob_0
print "P VALUE M: "
print prob_M
print "\n\n\n"

