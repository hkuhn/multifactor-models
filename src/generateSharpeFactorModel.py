from pandas import *

# retrieve data locations
#	should be in the format 'ticker', 'path'
dataLocations = read_csv('config/dataLocations.csv', encoding='utf-8')

# read data and store in a data frame
#	master_returns_data
#		[ ticker vs date and adj close]
monthly_data = read_csv(dataLocations['path'].iloc[0])
master_returns_data = DataFrame(index=monthly_data['Date'], columns=dataLocations['ticker'])
for index, row in dataLocations.iterrows():
	monthly_data = read_csv(row['path'])
	returns = monthly_data.set_index('Date')['Adj Close'].to_dict()
	returns_series = Series(returns)
	master_returns_data[row['ticker']] = returns_series

# get market data
market_data = master_returns_data['SPY']

# compute parameters (betas, variance) of assets
for item in master_returns_data:
	asset_return_matrix = item[1]['Adj Close']