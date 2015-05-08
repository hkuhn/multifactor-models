from pandas import *
from numpy import *

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

# get estimations for parameters (beta, alpha, variance)
means = master_returns_data.mean()
covariance_matrix = master_returns_data.cov()

betas = covariance_matrix['SPY'] / covariance_matrix['SPY']['SPY']
alphas = means - betas * means['SPY']

# get error terms by checking predictions with actual
alpha_ones = ones((1, len(master_returns_data.index)))
alphas_matrix = alphas.as_matrix().reshape(len(alphas.index), 1)
betas_matrix = betas.as_matrix().reshape(len(betas.index), 1)
Rm = master_returns_data['SPY'].as_matrix().reshape(1, len(master_returns_data.index))

# the model
predicted_returns_matrix = multiply(alphas_matrix, alpha_ones) + betas_matrix * Rm
predicted_returns_matrix = predicted_returns_matrix.transpose()
predicted_returns = DataFrame(data=predicted_returns_matrix, index=master_returns_data.index, columns=master_returns_data.columns)

epsilon_returns = master_returns_data.subtract(predicted_returns).mean()


epsilon_matrix = epsilon_returns.as_matrix().reshape(len(epsilon_returns.index), 1)
variance =  multiply(multiply(epsilon_matrix, epsilon_matrix), 1.0/(len(master_returns_data.index) - 2.0))


print "TRAINING A SHARPE FACTOR MODEL COMPLETE: "
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


