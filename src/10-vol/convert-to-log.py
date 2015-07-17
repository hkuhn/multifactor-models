import sys
import os.path
import datetime
from pandas import *
from functools import reduce
from numpy import *

directory = "../../data/10-vol/stocks/"
outdir = "../../data/10-vol/log-daily/"

for item in os.listdir(directory):
	if not item.endswith(".csv"):
		continue
	price_data = read_csv(directory + item)
	price_data = price_data[["Date", "Adj Close"]]
	price_data = price_data.sort("Date")

	#daily_returns = price_data["Adj Close"].pct_change(periods=1, fill_method='pad', axis=0)
	daily_returns = log(price_data["Adj Close"] / price_data["Adj Close"].shift(1))
	price_data["Returns"] = daily_returns

	daily_returns = price_data[["Date", "Returns"]]
	daily_returns = daily_returns.reset_index(drop=True)
	daily_returns = daily_returns.fillna(0)

	#
	daily_returns_series = daily_returns.sort("Date")
	print "Exporting Daily Data for " + item
	daily_returns_series.to_csv(outdir + os.path.splitext(item)[0] + ".csv")
