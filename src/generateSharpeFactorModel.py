from pandas import *

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
	prices_series = Series(returns)
	master_price_data[row['ticker']] = prices_series

# get market data
master_price_data = master_price_data.sort()

# compute monthly returns data
master_returns_data = master_price_data.pct_change(periods=1, fill_method='pad')
