import sys
import os.path
import math
from pandas import *
from numpy import *
from classes import Portfolio
from classes import Position

#######################
# HEADER
#######################
beginning_date = 197107


#######################
# RETRIEVE DATA
#######################
datadir = "../../data/8-JT/monthly/"
base_source = "AA_monthly.csv"
master_returns_file = datadir + "00_master_returns.csv"

if os.path.isfile(master_returns_file):
	print "Master Data File Found. Retrieving File..."
	master_returns = read_csv(master_returns_file)
	master_returns = master_returns.drop("Unnamed: 0", axis=1)
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
	master_returns.to_csv(master_returns_file)
print "Data Retrieval Completed"


#######################
# SETUP EXPERIMENT
#######################
print "Initializing Portfolios"
portfolios = []
for k in range (3, 15, 3):
	for j in range(3, 15, 3):
		portfolios.append(Portfolio(j, k, "J: " + str(j) + ", K: " + str(k)))


#######################
# BEGIN EXPERIMENT
#######################
print "Beginning Experiment"
beginning_index = master_returns[master_returns['Date'] == beginning_date].index.tolist()[0]

#for t in range(beginning_index, len(master_returns)):
for t in range(beginning_index, len(master_returns)):
	date = master_returns["Date"].iloc[t]
	print "Current Date: " + str(date)
	print "Generating Deciles..."
	JQ1_returns = ((master_returns.iloc[t-2:t+1] + 1).prod(axis=0).pow(0.33333, axis=0) - 1).dropna()
	JQ2_returns = ((master_returns.iloc[t-5:t+1] + 1).prod(axis=0).pow(0.16667, axis=0) - 1).dropna()
	JQ3_returns = ((master_returns.iloc[t-8:t+1] + 1).prod(axis=0).pow(0.11111, axis=0) - 1).dropna()
	JQ4_returns = ((master_returns.iloc[t-11:t+1] + 1).prod(axis=0).pow(0.08333, axis=0) - 1).dropna()
	##
	# SORT RETURNS
	##
	JQ1_returns.sort(ascending=False)
	JQ2_returns.sort(ascending=False)
	JQ3_returns.sort(ascending=False)
	JQ4_returns.sort(ascending=False)
	##
	# REMOVE DATE ROW
	##
	JQ1_returns = JQ1_returns.drop("Date")
	JQ2_returns = JQ2_returns.drop("Date")
	JQ3_returns = JQ3_returns.drop("Date")
	JQ4_returns = JQ4_returns.drop("Date")
	##
	# GENERATE DECILES
	##
	JQ1_top_decile = JQ1_returns[0:int(math.ceil(len(JQ1_returns) / 10.0))]
	JQ1_bottom_decile = JQ1_returns[len(JQ1_returns) - int(math.ceil(len(JQ1_returns) / 10.0)):]
	JQ2_top_decile = JQ2_returns[0:int(math.ceil(len(JQ2_returns) / 10.0))]
	JQ2_bottom_decile = JQ2_returns[len(JQ2_returns) - int(math.ceil(len(JQ2_returns) / 10.0)):]
	JQ3_top_decile = JQ3_returns[0:int(math.ceil(len(JQ3_returns) / 10.0))]
	JQ3_bottom_decile = JQ3_returns[len(JQ3_returns) - int(math.ceil(len(JQ3_returns) / 10.0)):]
	JQ4_top_decile = JQ4_returns[0:int(math.ceil(len(JQ4_returns) / 10.0))]
	JQ4_bottom_decile = JQ4_returns[len(JQ4_returns) - int(math.ceil(len(JQ4_returns) / 10.0)):]
	##
	# MEASURE PERFORMANCE FOR MONTH T (UPDATES DONE AT END OF YEAR)
	# LIQUIDATE DEAD POSITIONS
	# ADD POSITIONS
	##
	print "Calculating Portfolio Returns and Liquidating Old Positions..."
	for portfolio in portfolios:
		portfolio.reducePositionLives()
		portfolio.calculateReturn(date, master_returns.iloc[t])
		portfolio.liquidate()
		if portfolio.getName() == "J: 3, K: 3":
			portfolio.addPosition(Position(JQ1_top_decile.index, JQ1_bottom_decile.index, 3))
		elif portfolio.getName() == "J: 3, K: 6":
			portfolio.addPosition(Position(JQ1_top_decile.index, JQ1_bottom_decile.index, 6))
		elif portfolio.getName() == "J: 3, K: 9":
			portfolio.addPosition(Position(JQ1_top_decile.index, JQ1_bottom_decile.index, 9))
		elif portfolio.getName() == "J: 3, K: 12":
			portfolio.addPosition(Position(JQ1_top_decile.index, JQ1_bottom_decile.index, 12))
		elif portfolio.getName() == "J: 6, K: 3":
			portfolio.addPosition(Position(JQ2_top_decile.index, JQ2_bottom_decile.index, 3))
		elif portfolio.getName() == "J: 6, K: 6":
			portfolio.addPosition(Position(JQ2_top_decile.index, JQ2_bottom_decile.index, 6))
		elif portfolio.getName() == "J: 6, K: 9":
			portfolio.addPosition(Position(JQ2_top_decile.index, JQ2_bottom_decile.index, 9))
		elif portfolio.getName() == "J: 6, K: 12":
			portfolio.addPosition(Position(JQ2_top_decile.index, JQ2_bottom_decile.index, 12))
		elif portfolio.getName() == "J: 9, K: 3":
			portfolio.addPosition(Position(JQ3_top_decile.index, JQ3_bottom_decile.index, 3))
		elif portfolio.getName() == "J: 9, K: 6":
			portfolio.addPosition(Position(JQ3_top_decile.index, JQ3_bottom_decile.index, 6))
		elif portfolio.getName() == "J: 9, K: 9":
			portfolio.addPosition(Position(JQ3_top_decile.index, JQ3_bottom_decile.index, 9))
		elif portfolio.getName() == "J: 9, K: 12":
			portfolio.addPosition(Position(JQ3_top_decile.index, JQ3_bottom_decile.index, 12))
		elif portfolio.getName() == "J: 12, K: 3":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 3))
		elif portfolio.getName() == "J: 12, K: 6":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 6))
		elif portfolio.getName() == "J: 12, K: 9":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 9))
		elif portfolio.getName() == "J: 12, K: 12":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 12))

##
# SUMMARIZE RESULTS
##
results = DataFrame(portfolios[0].getPortfolioReturns().items(), columns=['Date', portfolios[0].getName()])
for i in range(1, len(portfolios)):
	inp = DataFrame(portfolios[i].getPortfolioReturns().items(), columns=['Date', portfolios[i].getName()])
	results = merge(results, inp, how="left", on="Date")

results = results.sort("Date")
print results.mean()
print results.mean() / results.sem(axis=0)



