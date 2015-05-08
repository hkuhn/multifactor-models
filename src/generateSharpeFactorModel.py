from pandas import *

# retrieve data locations
#	should be in the format 'ticker', 'path'
dataLocations = read_csv('config/dataLocations.csv', encoding='utf-8')

# read data and store in a data frame
#	master_returns_data
#		[[ticker (object)], [csv data (DataFrame)]]
master_returns_data = []
for index, row in dataLocations.iterrows():
	monthly_data = read_csv(row['path'])
	new_row = [row['ticker'], monthly_data]
	master_returns_data.append(new_row)


