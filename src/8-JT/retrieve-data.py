from pandas import *
import urllib
import urllib2

# get stock list
stocks = read_csv('../../data/8-JT/companylist.csv')
# get interval
start_month = "06"
start_day = "01"
start_year = "1962"
end_month = "06"
end_day = "01"
end_year = "1989"


for symbol in stocks["Symbol"]:
	testfile = urllib.URLopener()
	url = "http://ichart.finance.yahoo.com/table.csv?s=" + symbol + \
		"&a=" + start_month + "&b=" + start_day + "&c=" + start_year + \
		"&d=" + end_month + "&e=" + end_day + "&f=" + end_year + \
		"&g=d&ignore=.csv"
	try:
		testfile.retrieve(url, "./../../data/8-JT/stocks/" + symbol + ".csv")
	except IOError:
		print symbol + " ERROR"
		pass




