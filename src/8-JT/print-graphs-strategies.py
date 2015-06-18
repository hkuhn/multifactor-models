import sys
import os.path
import math
from pandas import *
from numpy import *
from classes import Portfolio
from classes import Position
import matplotlib.pyplot as plt 
import statsmodels.api as sm


beginning_date = 196501
ending_date = 200912


datadir = "../../data/8-JT/monthly/"
base_source = "AA_monthly.csv"
master_returns_file = datadir + "00_master_returns.csv"


master_returns = read_csv(master_returns_file)
jk_results = read_csv('./jk_results.csv')
blitz_results = read_csv('./blitz_results.csv')

master_beginning_index = master_returns[master_returns['Date'] == beginning_date].index.tolist()[0]
master_ending_index = master_returns[master_returns['Date'] == ending_date].index.tolist()[0]

blitz_beginning_index = blitz_results[blitz_results['Date'] == beginning_date].index.tolist()[0]
blitz_ending_index = blitz_results[blitz_results['Date'] == ending_date].index.tolist()[0]

jk_beginning_index = jk_results[jk_results['Date'] == beginning_date].index.tolist()[0]
jk_ending_index = jk_results[jk_results['Date'] == ending_date].index.tolist()[0]


benchmark = {str(int(beginning_date)): 1}
for t in range(master_beginning_index+1, master_ending_index):
	benchmark[str(int(master_returns.iloc[t]["Date"]))] = benchmark[str(int(master_returns.iloc[t-1]["Date"]))] * (1 + master_returns.iloc[t][2:].sum() / float(len(master_returns)))

jk_value = {str(int(beginning_date)): 1}
for t in range(jk_beginning_index+1, jk_ending_index):
	jk_value[str(int(jk_results.iloc[t]["Date"]))] = jk_value[str(int(jk_results.iloc[t-1]["Date"]))] * (1+jk_results.iloc[t]["J: 12, K: 3"])

blitz_value = {str(int(beginning_date)): 1}
for t in range(blitz_beginning_index+1, blitz_ending_index):
	blitz_value[str(int(blitz_results.iloc[t]["Date"]))] = blitz_value[str(int(blitz_results.iloc[t-1]["Date"]))] * (1+blitz_results.iloc[t]["J: 12-1M, K: 3"])


jk_value_frame = Series(jk_value)
blitz_value_frame = Series(blitz_value)
benchmark_frame = Series(benchmark)
plt.figure()
blitz_value_frame.plot(title="J: 12, K: 3 Value of $1");
jk_value_frame.plot()
#benchmark_frame.plot()
plt.show()


