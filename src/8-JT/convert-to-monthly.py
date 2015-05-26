import sys
import os.path
import datetime
from pandas import *
from functools import reduce
from numpy import *

directory = "../../data/8-JT/stocks/"
outdir = "../../data/8-JT/monthly/"

for item in os.listdir(directory):
	if not item.endswith(".csv"):
		continue
	price_data = read_csv(directory + item)
	price_data = price_data[["Date", "Adj Close"]]
	price_data = price_data.sort("Date")

	daily_returns = price_data["Adj Close"].pct_change(periods=1, fill_method='pad', axis=0)
	price_data["Returns"] = daily_returns

	daily_returns = price_data[["Date", "Returns"]]
	daily_returns = daily_returns.reset_index(drop=True)
	daily_returns = daily_returns.fillna(0)

	# start at first date and go up to end of month to get monthly return
	return_chain = []
	current_period = ""
	monthly_returns = {}
	for index, row in daily_returns.iterrows():
		current_date = row["Date"]
		current_return = row["Returns"]
		# set current period
		if current_period is "":
			current_period = current_date[0:4] + current_date[5:7]
		# drop all returns if month restarts and is not long enough
		if current_date[5:7] != current_period[4:6] and len(return_chain) < 10:
			return_chain = []
			current_period = current_date[0:4] + current_date[5:7]
		# if the current date has a different month and daily returns exceed ten days
		#	compute compound monthly return 
		#	store monthly return
		#	update current month
		#	reset the return chain
		if current_date[5:7] != current_period[4:6] and len(return_chain) >= 10:
			return_chain = [x + 1.0 for x in return_chain]
			monthly_return = reduce(lambda x, y: x*y, return_chain) - 1
			monthly_returns[current_period] = monthly_return
			return_chain = []
			current_period = ""
		# append return to chain
		return_chain.append(current_return)

	if len(monthly_returns.items()) > 0:
		monthly_return_series = DataFrame(monthly_returns.items(), columns=["Date", "Return"])
		monthly_return_series = monthly_return_series.sort("Date")
		print "Exporting Monthly Data for " + item
		monthly_return_series.to_csv(outdir + os.path.splitext(item)[0] + "_monthly.csv")
	else:
		print "SKIPPING EXPORT. NOT ENOUGH DATA: " + item
