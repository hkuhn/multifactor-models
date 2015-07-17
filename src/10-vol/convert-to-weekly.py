import sys
import os.path
import datetime
from pandas import *
from numpy import *

directory = "../../data/10-vol/log-daily/"
outdir = "../../data/10-vol/log-weekly/"

for item in os.listdir(directory):
	if not item.endswith(".csv"):
		continue
	daily_returns = read_csv(directory + item)
	daily_returns = daily_returns.drop("Unnamed: 0", axis=1)

	# start at first date and go up to end of month to get monthly return
	return_chain = []
	current_period = ""
	weekly_rets = {}
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
			ret_buckets = [return_chain[i:i+5] for i in range(0, len(return_chain), 5)]
			if len(ret_buckets[-1]) < 5:
				ret_buckets[-2] = ret_buckets[-2] + ret_buckets[-1]
				ret_buckets = ret_buckets[:-1]
			i = 1
			for week in ret_buckets:
				weekly_rets[current_period + str(i)] = sum(week)
				i = i + 1
			return_chain = []
			current_period = ""
		# append return to chain
		return_chain.append(current_return)

	if len(weekly_rets.items()) > 0:
		weekly_rets_series = DataFrame(weekly_rets.items(), columns=["Date", "Return"])
		weekly_rets_series = weekly_rets_series.sort("Date").reset_index(drop=True)
	else:
		print "SKIPPING EXPORT. NOT ENOUGH DATA: " + item
		continue

	# repeat the iteration to get 3-year volatility from weekly returns
	# need data for each month
	return_chain = []
	current_period = ""
	three_year_vol = {}
	for index, row in weekly_rets_series.iterrows():
		try:
			date = row["Date"][:-1]
			vol_beginning_index = weekly_rets_series[weekly_rets_series['Date'] == str(int(date[0:4]) - 3) + date[4:6] + "1"].index.tolist()[0]
			vol_ending_index = weekly_rets_series[weekly_rets_series['Date'] == date + "1"].index.tolist()[0]
			window_rets = weekly_rets_series.iloc[vol_beginning_index:vol_ending_index].dropna(axis=1)
			window_rets = window_rets.drop("Date", axis=1)
			window_std = std(window_rets)["Return"]
			three_year_vol[date] = window_std
		except:
			continue

	if len(three_year_vol.items()) > 0:
		print "Exporting Weekly Volatility Data for " + item
		vol_series = DataFrame(three_year_vol.items(), columns=["Date", "Volatility"])
		vol_series = vol_series.sort("Date")
		vol_series.to_csv(outdir + os.path.splitext(item)[0] + ".csv")
	else:
		print "SKIPPING EXPORT. NOT ENOUGH DATA: " + item



