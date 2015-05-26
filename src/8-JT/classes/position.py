class Position:
###################
# HEADER
###################
	'The position class that manages long constituents, short constituents and remaining life'

###################
# INHERENT VARS
###################
	#long constituents list
	#	list of names of constituents the position is long in
	# short constituents list
	#	list of names of constituents the position is short in
	# remaining life
	#	number of iterations left in this position before liquidation

###################
# CONSTRUCTOR
###################
	def __init__(self, long_const, short_const, life):
		self.long_constituents = long_const
		self.short_constituents = short_const
		self.remaining_life = life

###################
# METHODS
###################
	def calculateReturn(self, date, returns_row):
		long_returns = returns_row[self.long_constituents]
		short_returns = returns_row[self.short_constituents]
		if float(len(long_returns)) + float(len(short_returns)) > 0:
			total_returns = (float(long_returns.sum()) - float(short_returns.sum())) / (float(len(long_returns)) + float(len(short_returns)))
		else:
			total_returns = 0
		return total_returns

	def calculateLongReturn(self, date, returns_row):
		long_returns = returns_row[self.long_constituents]
		if float(len(long_returns)) > 0:
			total_returns = (float(long_returns.sum())) / (float(len(long_returns)))
		else:
			total_returns = 0
		return total_returns

	def calculateShortReturn(self, date, returns_row):
		short_returns = returns_row[self.short_constituents]
		if float(len(short_returns)) > 0:
			total_returns = (float(short_returns.sum())) / (float(len(short_returns)))
		else:
			total_returns = 0
		return total_returns

	def reduceLife(self):
		self.remaining_life -= 1

###################
# GETTERS/SETTERS
###################	
	def getRemainingLife(self):
		return self.remaining_life

	def getLongConstituents(self):
		return self.long_constituents

	def getShortConstituents(self):
		return self.short_constituents

	def setLongConstituents(self, long_const):
		self.long_constituents = long_const

	def setShortConstituents(self, short_const):
		self.short_constituents = short_const




