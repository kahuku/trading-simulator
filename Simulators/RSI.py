from yahoofinancials import YahooFinancials
import datetime
import pandas as pd

# TODO: make RSI Value (30) a parameter
# TODO: make turnaround time (2 days) a parameter

# If RSI drops below 30, buy, and sell two days later
class RSI:
	def __init__(self, startingValue, ticker, timeframe, period, rsi_window, turnaround_days, rsi_value):
		super().__init__()
		self.startingValue = startingValue
		self.ticker = ticker
		self.timeframe = timeframe
		self.period = period
		self.rsi_window = rsi_window
		self.turnaround_days = turnaround_days
		self.rsi_value = rsi_value

		self.prices = self.getPrices()
		self.rsi = self.getRSI(self.prices)
		self.values = [self.startingValue]
		self.originalValues = [self.startingValue]

	def simulate(self):
		print("Simulating!")
		for i in range(len(self.prices) - self.turnaround_days):
			if self.rsi[i] < self.rsi_value:
				# buy
				firstPrice = float('{0:.2f}'.format(self.prices[i]))
				secondPrice = float('{0:.2f}'.format(self.prices[i + self.turnaround_days]))
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
			startDate = today - datetime.timedelta(days=self.timeframe) - datetime.timedelta(days=self.rsi_window)
		elif self.period == "month":
			startDate = today - datetime.timedelta(weeks=4*self.timeframe) - datetime.timedelta(days=self.rsi_window)
		elif self.period == "year":
			startDate = today - datetime.timedelta(weeks=52*self.timeframe) - datetime.timedelta(days=self.rsi_window)

		yf = YahooFinancials(self.ticker.upper())
		data = yf.get_historical_price_data(str(startDate), str(today), 'daily')[self.ticker]['prices']
		return [date['adjclose'] for date in data]

	def getRSI(self, prices):
		price_diff = pd.Series(prices).diff()
		gains = price_diff.where(price_diff > 0, 0)
		losses = -price_diff.where(price_diff < 0, 0)
		avg_gain = gains.rolling(window=self.rsi_window).mean()
		avg_loss = losses.rolling(window=self.rsi_window).mean()
		rs = avg_gain / avg_loss
		rsi = 100 - (100 / (1 + rs))
		return rsi
