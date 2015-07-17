import sys
import os.path
import math
from pandas import *
from numpy import *
from classes import Portfolio
from classes import Position
import matplotlib.pyplot as plt 
import statsmodels.api as sm

#######################
# HEADER
#######################
beginning_date = 198512
ending_date = 200601

#######################
# RETRIEVE DATA
#######################
datadir = "../../data/10-vol/"
base_source = "AA.csv"
monthly_returns_file = datadir + "log-monthly/00_master_returns.csv"
weekly_vol_file = datadir + "log-weekly/00_master_volatility.csv"

# Retrieve returns
if os.path.isfile(monthly_returns_file):
	print "Master Returns File Found. Retrieving File..."
	master_returns = read_csv(monthly_returns_file)
	master_returns = master_returns.drop("Unnamed: 0", axis=1)
else:
	master_returns = read_csv(datadir + "log-monthly/" + base_source)
	master_returns = master_returns.drop("Return", axis=1)
	master_returns = master_returns.drop("Unnamed: 0", axis=1)
	print "No Master Returns Found. Retrieving Data..."
	for item in os.listdir(datadir + "log-monthly/"):
		if not item.endswith(".csv"):
			continue
		returns_data = read_csv(datadir + "log-monthly/" + item)
		returns_data = returns_data[["Date", "Return"]]
		if "Unnamed: 0" in returns_data.columns:
			returns_data = returns_data.drop("Unnamed: 0", axis=1)
		returns_data.rename(columns={'Return':os.path.splitext(item)[0]}, inplace=True)
		master_returns = merge(master_returns, returns_data, how="left", on="Date")
	master_returns.to_csv(monthly_returns_file)

# Retrieve Volatility
if os.path.isfile(weekly_vol_file):
	print "Master Volatility File Found. Retrieving File..."
	master_volatility = read_csv(weekly_vol_file)
	master_volatility = master_volatility.drop("Unnamed: 0", axis=1)
else:
	master_volatility = read_csv(datadir + "log-weekly/" + base_source)
	master_volatility = master_volatility.drop("Volatility", axis=1)
	master_volatility = master_volatility.drop("Unnamed: 0", axis=1)
	print "No Master Volatility Found. Retrieving Data..."
	for item in os.listdir(datadir + "log-weekly/"):
		if not item.endswith(".csv"):
			continue
		volatility_data = read_csv(datadir + "log-weekly/" + item)
		volatility_data = volatility_data[["Date", "Volatility"]]
		if "Unnamed: 0" in volatility_data.columns:
			volatility_data = volatility_data.drop("Unnamed: 0", axis=1)
		volatility_data.rename(columns={'Volatility':os.path.splitext(item)[0]}, inplace=True)
		master_volatility = merge(master_volatility, volatility_data, how="left", on="Date")
	master_volatility.to_csv(weekly_vol_file)

print "Data Retrieval Completed"





#######################
# SETUP EXPERIMENT
#######################
portfolio = Portfolio(36, 1, "Low Volatility Portfolio, Rebalanced Monthly")
portfolioD1 = Portfolio(36, 1, "Low Decile Volatility Portfolio, Rebalanced Monthly")
portfolioD10 = Portfolio(36, 1, "High Decile Volatility Portfolio, Rebalanced Monthly")


#######################
# BEGIN EXPERIMENT
#######################
print "Beginning Experiment"
beginning_index = master_returns[master_returns['Date'] == beginning_date].index.tolist()[0]
ending_index = master_returns[master_returns['Date'] == ending_date].index.tolist()[0]

for t in range(beginning_index, ending_index):
	date = master_returns["Date"].iloc[t]
	print "Current Date: " + str(date)
	print "Generating Deciles..."
	##
	# Get 3-Year Volatility Data
	##
	vol_index = master_volatility[master_volatility['Date'] == date].index.tolist()[0]
	window_vol = master_volatility.iloc[vol_index].dropna()
	window_vol = window_vol[(window_vol != 0)]
	window_vol = window_vol.drop("Date")
	window_vol.sort(ascending=True)
	##
	# Get Deciles
	##
	top_decile = window_vol[0:int(math.ceil(len(window_vol) / 10.0))]
	bottom_decile = window_vol[len(window_vol) - int(math.ceil(len(window_vol) / 10.0)):]
	##
	# Portfolio Manipulations
	##
	portfolio.reducePositionLives()
	portfolio.calculateReturn(date, master_returns.iloc[t])
	portfolio.liquidate()
	portfolio.addPosition(Position(top_decile.index, bottom_decile.index, 1))

	portfolioD1.reducePositionLives()
	portfolioD1.calculateReturn(date, master_returns.iloc[t])
	portfolioD1.liquidate()
	portfolioD1.addPosition(Position(top_decile.index, [], 1))

	portfolioD10.reducePositionLives()
	portfolioD10.calculateReturn(date, master_returns.iloc[t])
	portfolioD10.liquidate()
	portfolioD10.addPosition(Position(bottom_decile.index, [], 1))
	
	

##
# SUMMARIZE RESULTS
##
results = DataFrame(portfolio.getPortfolioReturns().items(), columns=['Date', portfolio.getName()])
results = results.sort("Date")
print results.mean()
print results.mean() / results.sem(axis=0)
results.to_csv('./vol_results.csv')

results = DataFrame(portfolioD1.getPortfolioReturns().items(), columns=['Date', portfolioD1.getName()])
results = results.sort("Date")
print results.mean()
print results.mean() / results.sem(axis=0)
results.to_csv('./vol_results_D1.csv')

results = DataFrame(portfolioD10.getPortfolioReturns().items(), columns=['Date', portfolioD10.getName()])
results = results.sort("Date")
print results.mean()
print results.mean() / results.sem(axis=0)
results.to_csv('./vol_results_D10.csv')











