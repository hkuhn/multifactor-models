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
beginning_date = 196501
ending_date = 201001


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

factor_returns_file = datadir + "mkt-smb-hml-rf.csv"
if os.path.isfile(master_returns_file):
	factor_returns = read_csv(factor_returns_file)
else:
	"Factor Returns file not found... Quitting..."
	sys.exit("Exit")


print "Data Retrieval Completed"


#######################
# SETUP EXPERIMENT
#######################
print "Initializing Portfolios"
portfolios = []
for k in range (3, 15, 3):
	portfolios.append(Portfolio(12, k, "J: 12-1M" + ", K: " + str(k)))


#######################
# BEGIN EXPERIMENT
#######################
print "Beginning Experiment"
beginning_index = master_returns[master_returns['Date'] == beginning_date].index.tolist()[0]
ending_index = master_returns[master_returns['Date'] == ending_date].index.tolist()[0]

#for t in range(beginning_index, len(master_returns)):
for t in range(beginning_index, ending_index):
	date = master_returns["Date"].iloc[t]
	print "Current Date: " + str(date)
	print "Generating Deciles..."
	JQ4_returns = master_returns.iloc[t-11:t].dropna(axis=1)
	factor_index = factor_returns[factor_returns['Date'] == date].index.tolist()[0]
	JQ4_factor_returns = factor_returns.iloc[factor_index-11:factor_index] / 100.0
	##
	# REMOVE DATE ROW
	##
	JQ4_returns = JQ4_returns.drop("Date", axis=1)
	JQ4_factor_returns = JQ4_factor_returns.drop("Date", axis=1)
	##
	# RUN FACTOR MODEL REGRESSION
	##
	window_factor_returns = factor_returns.iloc[factor_index-35:factor_index+1].drop("Date", axis=1) / 100.0
	window_realized_returns = master_returns.iloc[t-35:t+1].dropna(axis=1).drop("Date", axis=1)
	result_list = {}
	for index in window_realized_returns.keys():
		X = transpose(array([window_factor_returns["Mkt-RF"], window_factor_returns["SMB"], window_factor_returns["HML"]]))
		y = window_realized_returns.reset_index()[index].sub(window_factor_returns.reset_index()["RF"])
		X = sm.add_constant(X)
		result = sm.OLS(y, X).fit()
		expected_returns = JQ4_factor_returns.drop("RF", axis=1).multiply(array([result.params.x1, result.params.x2, result.params.x3]), axis=1).sum(axis=1) + result.params.const
		result_list[index] = expected_returns


	##
	# RETRIEVE RESIDUAL RETURNS
	##
	expected_returns = DataFrame(result_list)
	residual_returns = JQ4_returns.reset_index().sub(JQ4_factor_returns.reset_index()["RF"], axis=0).sub(expected_returns.reset_index()).drop("index", axis=1)
	residual_means = ((residual_returns + 1).prod(axis=0) - 1).dropna()
	#residual_means = residual_returns.mean()
	residual_stdev = residual_returns.std()
	ranked_list = residual_means / residual_stdev
	ranked_list.sort(ascending=False)
	##
	# GENERATE DECILES
	##
	JQ4_top_decile = ranked_list[0:int(math.ceil(len(ranked_list) / 10.0))]
	JQ4_bottom_decile = ranked_list[len(ranked_list) - int(math.ceil(len(ranked_list) / 10.0)):]
	JQ4_bottom_decile = JQ4_bottom_decile[JQ4_bottom_decile < 0]
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
		if portfolio.getName() == "J: 12-1M, K: 3":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 3))
		elif portfolio.getName() == "J: 12-1M, K: 6":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 6))
		elif portfolio.getName() == "J: 12-1M, K: 9":
			portfolio.addPosition(Position(JQ4_top_decile.index, JQ4_bottom_decile.index, 9))
		elif portfolio.getName() == "J: 12-1M, K: 12":
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
results.to_csv('./blitz_results.csv')

# value = {str(int(beginning_date)): 1}
# for t in range(1, len(results)):
# 	value[str(int(results.iloc[t]["Date"]))] = value[str(int(results.iloc[t-1]["Date"]))] * (1+results.iloc[t]["J: 12-1M, K: 3"])

# benchmark = {str(int(beginning_date)): 1}
# for t in range(beginning_index+1, ending_index):
# 	benchmark[str(int(master_returns.iloc[t]["Date"]))] = benchmark[str(int(master_returns.iloc[t-1]["Date"]))] * (1 + master_returns.iloc[t][1:].sum() / float(len(master_returns)))

# value_frame = Series(value)
# benchmark_frame = Series(benchmark)
# plt.figure(); value_frame.plot(title="J: 12-1M, K: 3 Value of $1");
# benchmark_frame.plot()
# plt.show()





