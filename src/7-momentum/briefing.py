from pandas import *
from numpy import *

#params
N = 500
T = 500
sigma = 0.5
rho = 0.05


stocks_array = DataFrame(data=ones((T,N)), columns=range(0, N), index=range(0, T))

for index, row in stocks_array[1:].iterrows():
	err = sigma * random.randn(N)
	r = rho * stocks_array[index-1] + err
	stocks_array[index] = r


winning_portfolio = []
losing_portfolio = []


for t in range(2, T):
	Randpast = stocks_array.loc[:,t-1:t]
	placeholder = Randpast.copy()
	placeholder = Randpast.sort(t-1)
	winning_portfolio.append(placeholder[t][450:].dropna().mean())
	losing_portfolio.append(placeholder[t][0:50].dropna().mean())

winning_portfolio = vstack(winning_portfolio)
losing_portfolio = vstack(losing_portfolio)

mean_winner = winning_portfolio.mean()
mean_loser = losing_portfolio.mean()

stdev_winner = winning_portfolio.std()
stdev_loser = losing_portfolio.std()

sr_winner = mean_winner / stdev_winner
sr_loser = mean_loser / stdev_loser