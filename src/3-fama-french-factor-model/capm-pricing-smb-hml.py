
from pandas import *
from numpy import *
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt 

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

# get estimations of parameters
means = monthly_returns.mean()
covariance_matrix = monthly_returns.cov()

betas = covariance_matrix['Rm- Rf'] / covariance_matrix['Rm- Rf']['Rm- Rf']
alphas = means - betas * means['Rm- Rf']

print "TRAINING A SHARPE FACTOR MODEL COMPLETE: "
print "Parameters Learned: "
print "\n\n\n\n"
print "Alphas: "
print DataFrame(data=[alphas], index=["alphas"], columns=alphas.index)
print "\n\n\n\n"
print "Betas: "
print DataFrame(data=[betas], index=["betas"], columns=betas.index)
print "\n\n\n\n"

# TESTING PHASE
#	Testing if the beta factor are priced in the cross-section
#	Use the beta trained to estimate return on test data
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)
betas_matrix = betas.as_matrix().reshape(len(betas.index), 1)

testing_ones = ones((1, len(monthly_returns.index)))
Rm_testing = monthly_returns['Rm- Rf'].as_matrix().reshape(1, len(monthly_returns.index))
testing_predicted_returns_matrix = multiply(alphas_matrix, testing_ones) + betas_matrix * Rm_testing
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


# PLOTTING
plotting_data = monthly_returns.loc[:,['SMB', 'HML', 'Rm- Rf']]
plotting_data["Rm- Rf"]
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(plotting_data["Rm- Rf"], plotting_data["HML"], c='b', marker='s', label="HML")
ax1.scatter(plotting_data["Rm- Rf"], plotting_data["SMB"], c='r', marker='o', label="SMB")
#plotting_data.plot(x="Rm- Rf", y="HML", kind="scatter")
line_plot = linspace(-20,20,600)
ax1.plot(line_plot, line_plot*betas["SMB"] + alphas["SMB"], c='r')
#plotting_data.plot(x="Rm- Rf", y="SMB", kind="scatter")
another_line_plot = linspace(-20,20,600)
ax1.plot(another_line_plot, another_line_plot*betas["HML"] + alphas["HML"], c='b')
plt.legend(loc='upper left')
plt.show()

