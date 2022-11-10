import datetime
import yfinance as yf

# If price dropped in last 30 minutes of day, buy close and sell on open
class Flip30:
	def __init__(self, startingValue, ticker, timeframe, period):
		super().__init__()
		self.startingValue = startingValue
		self.ticker = ticker
		self.timeframe = timeframe
		self.period = period

		self.prices30, self.pricesClose = self.getPrices()
		self.originalValues = []
		self.values = []

	def simulate(self):
		print("Simulating!")
		self.originalValues = self.getOriginalValues()

		return ["new"], ["original"]

	def getOriginalValues(self):
		breakpoint()

	def getPrices(self):
		# 13 and 14
		data = yf.Ticker(self.ticker.upper()).history(period="1mo", interval="30m")
		breakpoint()
