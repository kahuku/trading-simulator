import datetime
import time
from yahoofinancials import YahooFinancials

class BCSO:
	def __init__(self, startingValue, ticker, timeframe, period):
		super().__init__()
		self.startingValue = startingValue
		self.ticker = ticker
		self.timeframe = timeframe
		self.period = period

		self.prices = self.getPrices()
		self.values = [self.startingValue]
		self.originalValues = [self.startingValue]

	def simulate(self):
		print("Simulating!")

		for i in range(1, len(self.prices) - 1):
			firstPrice = float('{0:.2f}'.format(self.prices[i - 1]['close']))
			secondPrice = float('{0:.2f}'.format(self.prices[i]['open']))
			percentChange = (secondPrice - firstPrice) / firstPrice
			self.values.append(self.values[-1] * (1 + percentChange))

			firstPrice = float('{0:.2f}'.format(self.prices[i - 1]['close']))
			secondPrice = float('{0:.2f}'.format(self.prices[i]['close']))
			percentChange = (secondPrice - firstPrice) / firstPrice
			self.originalValues.append(self.originalValues[-1] * (1 + percentChange))

		return self.values, self.originalValues

	def getPrices(self):
		today = datetime.date.today()
		if self.period == "day":
			startDate = today - datetime.timedelta(days=self.timeframe)
		elif self.period == "month":
			startDate = today - datetime.timedelta(weeks=4*self.timeframe)
		elif self.period == "year":
			startDate = today - datetime.timedelta(weeks=52*self.timeframe)

		yf = YahooFinancials(self.ticker.upper())
		return yf.get_historical_price_data(str(startDate), str(today), 'daily')[self.ticker]['prices']
