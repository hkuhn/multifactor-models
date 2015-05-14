
from pandas import *
from numpy import *
from scipy import stats
import statsmodels.api as sm

beginning_date = 196401
ending_date = 201201

# ESTIMATE BETAS
# retrieve data and select data from 1964 to 2011
monthly_returns = read_csv('../../data/2-assessment-of-single-factor-model/monthly-equal-weighted-returns.csv')
benchmark_monthly_returns = read_csv('../../data/2-assessment-of-single-factor-model/monthly-benchmark-returns.csv')
size = read_csv('../../data/2-assessment-of-single-factor-model/size.csv')

beginning_index = monthly_returns[monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = monthly_returns[monthly_returns['Date'] == ending_date].index.tolist()
monthly_returns = monthly_returns[beginning_index[0]:ending_index[0]]

beginning_index = benchmark_monthly_returns[benchmark_monthly_returns['Date'] == beginning_date].index.tolist()
ending_index = benchmark_monthly_returns[benchmark_monthly_returns['Date'] == ending_date].index.tolist()
benchmark_monthly_returns = benchmark_monthly_returns[beginning_index[0]:ending_index[0]]

size = size[beginning_index[0]:ending_index[0]]

monthly_returns['Rm- Rf'] = benchmark_monthly_returns['Rm- Rf']
# remove date
monthly_returns = monthly_returns.ix[:,1:]
size = size.ix[:,1:]

# get estimations of parameters
means = monthly_returns.mean()
covariance_matrix = monthly_returns.cov()

betas = covariance_matrix['Rm- Rf'] / covariance_matrix['Rm- Rf']['Rm- Rf']

# RUN CROSS SECTION REGRESSION
betas = betas.ix[:-1]
monthly_returns = monthly_returns.ix[:,:-1]

betas_array = betas.as_matrix()
ln_size_array = size.as_matrix()
ln_size_array = log(size.as_matrix())


gamma_0 = []
gamma_M = []
gamma_ME = []
counter = 0
for index, row in monthly_returns.iterrows():
	cross_section_returns_array = row.as_matrix()
	instance_size_array = ln_size_array[counter]
	X = transpose(array([betas_array, instance_size_array]))
	counter += 1
	X = sm.add_constant(X)
	model = sm.OLS(cross_section_returns_array, X)
	model = model.fit()
	gamma_0.append(model.params[0])
	gamma_M.append(model.params[1])
	gamma_ME.append(model.params[2])


# retrieve average gammas
gamma_0_array = array(gamma_0)
gamma_0_array[isnan(gamma_0_array)] = 0
gamma_M_array = array(gamma_M)
gamma_M_array[isnan(gamma_M_array)] = 0
gamma_ME_array = array(gamma_ME)
gamma_ME_array[isnan(gamma_ME_array)] = 0
average_gamma_0 = average(gamma_0_array)
average_gamma_M = average(gamma_M_array)
average_gamma_ME = average(gamma_ME_array)
std_err_mean_0 = std(gamma_0_array) / sqrt(len(gamma_0))
std_err_mean_M = std(gamma_M_array) / sqrt(len(gamma_M))
std_err_mean_ME = std(gamma_ME_array) / sqrt(len(gamma_ME))

# T-Statistic Population Parameters
#	M should equal the market excess return
#	0 should equal the risk free rate
t_stat_0, prob_0 = stats.ttest_1samp(gamma_0_array, 0.0)
t_stat_M, prob_M = stats.ttest_1samp(gamma_M_array, means['Rm- Rf'])
t_stat_ME, prob_ME = stats.ttest_1samp(gamma_ME_array, 0.0)

print "QUESTION 1f: Cross Section Regression on Returns"
print "GAMMA 0: "
print average_gamma_0
print "GAMMA M: "
print average_gamma_M
print "GAMMA ME: "
print average_gamma_ME
print "\n"
print "STD ERR 0: "
print std_err_mean_0
print "STD ERR M: "
print std_err_mean_M
print "STD ERR ME: "
print std_err_mean_ME
print "T STATISTIC 0: "
print t_stat_0
print "T STATISTIC M: "
print t_stat_M
print "T STATISTIC ME: "
print t_stat_ME
print "P VALUE 0: "
print prob_0
print "P VALUE M: "
print prob_M
print "P VALUE ME: "
print prob_ME
print "\n\n\n"

