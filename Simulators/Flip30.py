import pandas as pd
import yfinance as yf

# If price dropped in last 30 minutes of day, buy close and sell on open
class Flip30:
	def __init__(self, startingValue, ticker, timeframe, period):
		super().__init__()
		self.startingValue = startingValue
		self.ticker = ticker
		self.timeframe = timeframe
		self.period = period

		self.getPrices()
		self.originalValues = [self.startingValue]
		self.values = [self.startingValue]

	def simulate(self):
		print("Simulating!")

		for i in range(1, len(self.pricesClose) - 1):
			price30, priceClose = self.prices30[i - 1], self.pricesClose[i - 1]
			if price30 > priceClose:
				# decreasing in last 30 minutes -- buy
				firstPrice = float('{0:.2f}'.format(self.pricesClose[i - 1]))
				secondPrice = float('{0:.2f}'.format(self.pricesOpen[i]))
				percentChange = (secondPrice - firstPrice) / firstPrice
				self.values.append(self.values[-1] * (1 + percentChange))
			else:
				# increasing in last 30 minutes -- don't buy
				self.values.append(self.values[-1])

			# we do the same thing with the buy and hold strategy no matter what
			firstPrice = float('{0:.2f}'.format(self.pricesClose[i - 1]))
			secondPrice = float('{0:.2f}'.format(self.pricesClose[i]))
			percentChange = (secondPrice - firstPrice) / firstPrice
			self.originalValues.append(self.originalValues[-1] * (1 + percentChange))

		print(len(self.values), len(self.pricesOpen))
		return self.values, self.originalValues

	def getPrices(self):
		data = yf.Ticker(self.ticker.upper()).history(period="1mo", interval="30m")
		data = data.reset_index()
		data["Datetime"] = pd.to_datetime(data["Datetime"], utc=True)
		data = data.groupby(pd.Grouper(key="Datetime", freq="1D")).nth([-2, -1, 1])
		self.prices30, self.pricesClose, self.pricesOpen = data[::3]["Close"].tolist(), data[1::3]["Close"].tolist(), data[2::3]["Close"].tolist()
