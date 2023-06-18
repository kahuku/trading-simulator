from yahoofinancials import YahooFinancials
import datetime
import pandas as pd

WINDOW = 14

# TODO: make RSI Value (30) a parameter
# TODO: make turnaround time (2 days) a parameter

# If RSI drops below 30, buy, and sell two days later
class RSI:
	def __init__(self, startingValue, ticker, timeframe, period):
		super().__init__()
		self.startingValue = startingValue
		self.ticker = ticker
		self.timeframe = timeframe
		self.period = period

		self.prices = self.getPrices()
		self.rsi = self.getRSI(self.prices)
		self.values = [self.startingValue]
		self.originalValues = [self.startingValue]

	def simulate(self):
		print("Simulating!")
		for i in range(len(self.prices) - 2):
			if self.rsi[i] < 30:
				# buy
				firstPrice = float('{0:.2f}'.format(self.prices[i]))
				secondPrice = float('{0:.2f}'.format(self.prices[i + 2]))
				percentChange = (secondPrice - firstPrice) / firstPrice
				self.values.append(self.values[-1] * (1 + percentChange))
			else:
				# don't buy
				self.values.append(self.values[-1])
			
			firstPrice = float('{0:.2f}'.format(self.prices[i]))
			secondPrice = float('{0:.2f}'.format(self.prices[i + 1]))
			percentChange = (secondPrice - firstPrice) / firstPrice
			self.originalValues.append(self.originalValues[-1] * (1 + percentChange))
		
		return self.values, self.originalValues

	def getPrices(self):
		today = datetime.date.today()
		if self.period == "day":
			startDate = today - datetime.timedelta(days=self.timeframe) - datetime.timedelta(days=WINDOW)
		elif self.period == "month":
			startDate = today - datetime.timedelta(weeks=4*self.timeframe) - datetime.timedelta(days=WINDOW)
		elif self.period == "year":
			startDate = today - datetime.timedelta(weeks=52*self.timeframe) - datetime.timedelta(days=WINDOW)

		yf = YahooFinancials(self.ticker.upper())
		data = yf.get_historical_price_data(str(startDate), str(today), 'daily')[self.ticker]['prices']
		return [date['adjclose'] for date in data]

	def getRSI(self, prices):
		price_diff = pd.Series(prices).diff()
		gains = price_diff.where(price_diff > 0, 0)
		losses = -price_diff.where(price_diff < 0, 0)
		avg_gain = gains.rolling(window=WINDOW).mean()
		avg_loss = losses.rolling(window=WINDOW).mean()
		rs = avg_gain / avg_loss
		rsi = 100 - (100 / (1 + rs))
		return rsi
