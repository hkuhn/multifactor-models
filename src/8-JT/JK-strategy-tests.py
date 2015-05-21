import sys
import os.path
from pandas import *
from numpy import *
from classes.object import Portfolio

#######################
# RETRIEVE DATA
#######################
datadir = "../../data/8-JT/monthly/"
base_source = "AA_monthly.csv"
master_returns_file = datadir + "00_master_returns.csv"

if os.path.isfile(master_returns_file):
	print "Master Data File Found. Retrieving File..."
	master_returns = read_csv(master_returns_file)
else:
	master_returns = read_csv(datadir + base_source)
	master_returns = master_returns.drop("Return", axis=1)
	master_returns = master_returns.drop("Unnamed: 0", axis=1)
	print "No Master File Found. Retrieving Data..."
	for item in os.listdir(datadir):
		if not item.endswith(".csv"):
			continue
		returns_data = read_csv(datadir + item)
		returns_data = returns_data[["Date", "Return"]]
		if "Unnamed: 0" in returns_data.columns:
			returns_data = returns_data.drop("Unnamed: 0", axis=1)
		returns_data.rename(columns={'Return':os.path.splitext(item)[0]}, inplace=True)
		master_returns = merge(master_returns, returns_data, how="left", on="Date")

print "Data Retrieval Completed"


#######################
# SETUP EXPERIMENT
#######################