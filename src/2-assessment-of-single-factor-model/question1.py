# Question 1:
#
#
from pandas import *
from numpy import *

beginning_date = 196401
ending_date = 201101

# ESTIMATE BETAS
# retrieve data and select data from 1964 to 2011
monthly_returns = read_csv('../../data/2-assessment-of-single-factor-model/monthly-equal-weighted-returns.csv', encoding='utf-8')
benchmark_monthly_returns = read_csv('../../data/2-assessment-of-single-factor-model/monthly-benchmark-returns.csv', encoding='utf-8')
beginning_index = monthly_returns[monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = monthly_returns[monthly_returns['Date'] == ending_date].index.tolist()
monthly_returns = monthly_returns['Date'][beginning_index[0]:ending_index[0]]
