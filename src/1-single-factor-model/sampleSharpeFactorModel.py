from pandas import *
import matplotlib


print "Running Experiment..."

r_squared_list = []
mse_list = []
betas_list = []
alphas_list = []
num_iterations = 100
for i in range(0, num_iterations):
	execfile("generateSharpeFactorModel.py")
	r_squared_list.append(r_squared)
	mse_list.append(mse_data)
	betas_list.append(betas)
	alphas_list.append(alphas)

mse_data_table = DataFrame(data=mse_list)
r_squared_table = DataFrame(data=r_squared_list)
betas_table = DataFrame(data=betas_list)
alphas_table = DataFrame(data=alphas_list)

print "\n\n\n\n\n\n"
print "TEST STATISTICS: "
print " Average MSE: "
print mse_data_table.mean()
print "\n\n"
print "Average R Squared: "
print r_squared_table.mean()
print "\n\n"
print "Average Alphas: "
print alphas_table.mean()
print "\n\n"
print "Average Betas: "
print betas_table.mean()


