import sys
import os.path
import math
from pandas import *
from numpy import *
from classes import Portfolio
from classes import Position
import matplotlib.pyplot as plt 
import statsmodels.api as sm


beginning_date = 198512
ending_date = 200512


datadir = "../../data/10-vol/log-monthly/"
base_source = "AA.csv"
master_returns_file = datadir + "00_master_returns.csv"
weekly_vol_file = "../../data/10-vol/log-weekly/00_master_volatility.csv"


master_returns = read_csv(master_returns_file)
D1results = read_csv('./vol_results_D1.csv')
D10results = read_csv('./vol_results_D10.csv')
results = read_csv('./vol_results.csv')
vol = read_csv(weekly_vol_file)
master_returns = master_returns[vol.columns.values]

master_beginning_index = master_returns[master_returns['Date'] == beginning_date].index.tolist()[0]
master_ending_index = master_returns[master_returns['Date'] == ending_date].index.tolist()[0]

beginning_index = results[results['Date'] == beginning_date].index.tolist()[0]
ending_index = results[results['Date'] == ending_date].index.tolist()[0]


benchmark = {str(int(beginning_date)): 1}
for t in range(master_beginning_index+1, master_ending_index):
	benchmark[str(int(master_returns.iloc[t]["Date"]))] = benchmark[str(int(master_returns.iloc[t-1]["Date"]))] + (master_returns.iloc[t][2:].dropna().sum() / float(len(master_returns)))

value = {str(int(beginning_date)): 1}
for t in range(beginning_index+1, ending_index):
	value[str(int(results.iloc[t]["Date"]))] = value[str(int(results.iloc[t-1]["Date"]))] + results.iloc[t]["Low Volatility Portfolio, Rebalanced Monthly"]

D1value = {str(int(beginning_date)): 1}
for t in range(beginning_index+1, ending_index):
	D1value[str(int(D1results.iloc[t]["Date"]))] = D1value[str(int(D1results.iloc[t-1]["Date"]))] + D1results.iloc[t]["Low Decile Volatility Portfolio, Rebalanced Monthly"]

D10value = {str(int(beginning_date)): 1}
for t in range(beginning_index+1, ending_index):
	D10value[str(int(D10results.iloc[t]["Date"]))] = D10value[str(int(D10results.iloc[t-1]["Date"]))] + D10results.iloc[t]["High Decile Volatility Portfolio, Rebalanced Monthly"]



value_frame = Series(value)
D1value_frame = Series(D1value)
D10value_frame = Series(D10value)
benchmark_frame = Series(benchmark)
plt.figure()
#value_frame.plot(title="Low Volatility Portfolio, Rebalanced Monthly - Value of $1");
D1value_frame.plot();
#D10value_frame.plot();
benchmark_frame.plot()
plt.show()


print "Sharpe Ratio of D1: " + str(mean(D1results).iloc[2] / std(D1results).iloc[2])
print "Mean Return of D1: " + str(mean(D1results).iloc[2])
print "Standard Deviation of D1: " + str(std(D1results).iloc[2])
print "T value: " + str((mean(D1results).iloc[2] / std(D1results).iloc[2]) * sqrt(len(D1results)))

print "Sharpe Ratio of D10: " + str(mean(D10results).iloc[2] / std(D10results).iloc[2])
print "Mean Return of D10: " + str(mean(D10results).iloc[2])
print "Standard Deviation of D10: " + str(std(D10results).iloc[2])
print "T value: " + str((mean(D10results).iloc[2] / std(D10results).iloc[2]) * sqrt(len(D10results)))

print "Sharpe Ratio of market: " + str(mean(master_returns).iloc[2] / std(master_returns).iloc[2])
print "Mean Return of market: " + str(mean(master_returns).iloc[2])
print "Standard Deviation of market: " + str(std(master_returns).iloc[2])
print "T value: " + str((mean(master_returns).iloc[2] / std(master_returns).iloc[2]) * sqrt(len(master_returns)))




