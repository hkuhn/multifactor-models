# PCA Factor Model
#	3-Factor Model Derived from PCA on 25 Portfolio's on size and value
#
#	Credit goes to CalculatingInvestor for setting up the experiment
#
beginning_date = "196401"
ending_date = "201112"


monthly_returns = read.csv('../../data/6-pca-factor-model/mkt-smb-hml-rf.csv')
input_data = read.csv('../../data/6-pca-factor-model/monthly-equal-weighted-returns.csv')


# filter data by Date
beginning_index = row.names(monthly_returns[which(monthly_returns$Date == beginning_date), ])
ending_index = row.names(monthly_returns[which(monthly_returns$Date == ending_date), ])
monthly_returns = monthly_returns[beginning_index:ending_index, ]
beginning_index = row.names(input_data[which(input_data$Date == beginning_date), ])
ending_index = row.names(input_data[which(input_data$Date == ending_date), ])
input_data = input_data[beginning_index:ending_index, ]

# remove date column
monthly_returns = monthly_returns[, 2:ncol(monthly_returns)]
input_data = input_data[, 2:ncol(input_data)]

# Calculate the covariance matrix on the input data
covariance = cov(input_data)

# Run eigenvalue decomposition on covariance matrix
# NOTE: already sorted
decomposition = eigen(covariance)
eigenvalues = decomposition$values
eigenvectors = decomposition$vectors
#barchart(sqrt(eigenvaues))

# retrieve factor loadings
factor_loadings = data.matrix(input_data) %*% data.matrix(eigenvectors)

# retrieve top 3 factors
f1 = factor_loadings[,1]
f2 = factor_loadings[,2]
f3 = factor_loadings[,3]


# retrieve test results using Fama French 3 Factor Model
X = data.matrix(monthly_returns[ c("Mkt.RF", "SMB", "HML") ])
for (index in colnames(input_data)) {
	y = data.matrix(input_data[index])
	regression_model = lm(y ~ X)
	print(index)
	print(summary(regression_model))
}

# retrieve test results using PCA 3 Factor Model
X = data.matrix(factor_loadings[,1:3])
for (index in colnames(input_data)) {
	y = data.matrix(input_data[index])
	regression_model = lm(y ~ X)
	print(index)
	print(summary(regression_model))
}



