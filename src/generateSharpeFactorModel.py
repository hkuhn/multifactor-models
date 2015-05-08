from pandas import *
from numpy import *
import random

# training testing proportions
training_size = 0.75
test_size = 1.0 - training_size
divisor = 10.0

# retrieve data locations
#	should be in the format 'ticker', 'path'
dataLocations = read_csv('config/dataLocations.csv', encoding='utf-8')

# read data and store in a data frame
#	master_price_data
#		[ ticker vs date and adj close]
monthly_data = read_csv(dataLocations['path'].iloc[0])
master_price_data = DataFrame(index=monthly_data['Date'], columns=dataLocations['ticker'])
for index, row in dataLocations.iterrows():
	monthly_data = read_csv(row['path'])
	prices = monthly_data.set_index('Date')['Adj Close'].to_dict()
	prices_series = Series(prices)
	master_price_data[row['ticker']] = prices_series

# get market data
master_price_data = master_price_data.sort()

# compute monthly returns data
master_returns_data = master_price_data.pct_change(periods=1, fill_method='pad')

# divide into training/testing
# randomize indices for unbiased training
index_list = random.sample(range(0,len(master_price_data.index),int(divisor)), int(len(master_price_data.index) / divisor))
num_train = int(floor(training_size * len(master_price_data.index)))
reference_training_list = index_list[:int(num_train/divisor)]
reference_testing_list = index_list[int(num_train/divisor):]
training_list = []
testing_list = []
for item in reference_training_list:
	for i in range (0,5):
		training_list.append(item + i)

for item in reference_testing_list:
	for i in range (0,5):
		testing_list.append(item + i)


training_returns_data = master_returns_data.iloc[training_list]
testing_returns_data = master_returns_data.iloc[testing_list]

# get estimations for parameters (beta, alpha, variance)
means = training_returns_data.mean()
covariance_matrix = training_returns_data.cov()

betas = covariance_matrix['SPY'] / covariance_matrix['SPY']['SPY']
alphas = means - betas * means['SPY']

# get error terms by checking predictions with actual
alpha_ones = ones((1, len(training_returns_data.index)))
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)
betas_matrix = betas.as_matrix().reshape(len(betas.index), 1)
Rm = training_returns_data['SPY'].as_matrix().reshape(1, len(training_returns_data.index))

# the model
predicted_returns_matrix = multiply(alphas_matrix, alpha_ones) + betas_matrix * Rm
predicted_returns_matrix = predicted_returns_matrix.transpose()
predicted_returns = DataFrame(data=predicted_returns_matrix, index=training_returns_data.index, columns=training_returns_data.columns)

epsilon_returns = training_returns_data.subtract(predicted_returns).mean()


epsilon_matrix = epsilon_returns.as_matrix().reshape(len(epsilon_returns.index), 1)
variance =  multiply(multiply(epsilon_matrix, epsilon_matrix), 1.0/(len(training_returns_data.index) - 2.0))


print "TRAINING A SHARPE FACTOR MODEL COMPLETE: "
print "number of training examples: " + str(num_train)
print "number of testing examples: " + str(len(master_price_data.index) - num_train)
print "Parameters Learned: "
print "\n\n\n\n"
print "Alphas: "
print DataFrame(data=[alphas], index=["alphas"], columns=alphas.index)
print "\n\n\n\n"
print "Betas: "
print DataFrame(data=[betas], index=["betas"], columns=betas.index)
print "\n\n\n\n"
print "Epsilon Returns: "
print DataFrame(data=[epsilon_returns], index=["epsilon"], columns=epsilon_returns.index)
print "\n\n\n\n"







# TESTING BETA PARAMETER ESTIMATION:
#	Test Beta by treating it as an independent variable
#	Solve for lambda_0, the factor premia not associated with our beta

testing_means = testing_returns_data.mean()
testing_covariance_matrix = testing_returns_data.cov()

testing_betas = testing_covariance_matrix['SPY'] / testing_covariance_matrix['SPY']['SPY']
testing_alphas = testing_means - testing_betas * testing_means['SPY']




# TESTING PHASE
#	Testing if the beta factor are priced in the cross-section
#	Use the beta trained to estimate return on test data
testing_ones = ones((1, len(testing_returns_data.index)))
Rm_testing = testing_returns_data['SPY'].as_matrix().reshape(1, len(testing_returns_data.index))
#testing_predicted_returns_matrix = multiply(alphas_matrix, testing_ones) + betas_matrix * Rm_testing + multiply(epsilon_matrix, testing_ones)
testing_predicted_returns_matrix = betas_matrix * Rm_testing
testing_predicted_returns_matrix = testing_predicted_returns_matrix.transpose()
testing_predicted_returns = DataFrame(data=testing_predicted_returns_matrix, index=testing_returns_data.index, columns=testing_returns_data.columns)
differences = testing_returns_data.subtract(testing_predicted_returns)
difference_between_mean = testing_returns_data.subtract(testing_returns_data.mean())

# mean squared error
ss_res = (differences ** 2).sum()
ss_tot = (difference_between_mean ** 2).sum()
r_squared = 1.0 - (ss_res / ss_tot)
mse_data = ss_res / (len(testing_returns_data.index))

print "TESTING RESULTS: "
print "R squared: "
print DataFrame(data=[r_squared], index=["r squared"], columns=r_squared.index)
print "\n\n\n\n"
print "MSE: "
print DataFrame(data=[mse_data], index=["MSE"], columns=mse_data.index)
print "\n\n\n\n"


