class Portfolio:
###################
# HEADER
###################
	'The portfolio class that manages positions and tracks portfolio returns'

###################
# INHERENT VARS
###################
	#positions list
	#	list of Position objects currently in the portfolio
	# returns array
	#	dict mapping date to portfolio return
	# J
	#	length measure for how far back we should look
	#	to calculate returns data for stock ranking
	# K
	#	length of time to hold a position
	# Name
	#	name of the portfolio

###################
# CONSTRUCTOR
###################
	def __init__(self, J, K, name):
		self.positions_list = []
		self.returns_array = {}
		self.J = J
		self.K = K
		self.name = name

###################
# METHODS
###################
	def addPosition(self, position):
		# check if security exists in any prior positions' similar row
		#	if it does, don't add it again
		#	if it doesn't, add it to new position
		# if long constituent exists in short constituent, remove position
		# if short constituent exists in long constituent, remove position
		# for prior_position in self.positions_list:
		# 	long_overlap = set(prior_position.getLongConstituents()) & set(position.getLongConstituents())
		# 	position.setLongConstituents([x for x in position.getLongConstituents() if x not in long_overlap])
		# 	short_overlap = set(prior_position.getShortConstituents()) & set(position.getShortConstituents())
		# 	position.setShortConstituents([x for x in position.getShortConstituents() if x not in short_overlap])
		# 	long_short_cross_overlap = set(prior_position.getLongConstituents()) & set(position.getShortConstituents())
		# 	prior_position.setLongConstituents([x for x in prior_position.getLongConstituents() if x not in long_short_cross_overlap])
		# 	short_long_cross_overlap = set(prior_position.getShortConstituents()) & set(position.getLongConstituents())
		# 	prior_position.setShortConstituents([x for x in prior_position.getShortConstituents() if x not in short_long_cross_overlap])
		self.positions_list.append(position)

	def liquidate(self):
		for position in self.positions_list:
			if position.getRemainingLife() <= 0:
				self.positions_list.remove(position)

	def calculateReturn(self, date, returns_row):
		portfolio_return_list = []
		for position in self.positions_list:
			position_return = position.calculateLongReturn(date, returns_row) - position.calculateShortReturn(date, returns_row)
			portfolio_return_list.append(position_return)
		if len(portfolio_return_list) > 0:
			portfolio_return = float(sum(portfolio_return_list)) / float(len(portfolio_return_list))
		else:
			portfolio_return = 0
		self.returns_array[date] = portfolio_return

	def reducePositionLives(self):
		for position in self.positions_list:
			position.reduceLife()

###################
# GETTERS/SETTERS
###################
	def getPositions(self):
		return self.positions_list

	def getPortfolioReturns(self):
		return self.returns_array

	def getName(self):
		return self.name

	def getK(self):
		return self.K

	def getJ(self):
		return self.J

