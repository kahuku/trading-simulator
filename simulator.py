from Simulators.BCSO import BCSO
from Simulators.Flip30 import Flip30
from Simulators.RSI import RSI

class Simulator:
	def __init__(self, params):
		super().__init__()

		self.strategy = params['strategy']
		self.timeframe = params['timeframe']
		self.period = params['period']
		self.ticker = params['ticker']
		self.startingValue = params['startingValue']

		if self.strategy == 'RSI Reversal':
			self.rsi_window = params['rsi_window']
			self.turnaround_days = params['turnaround_days']
			self.rsi_value = params['rsi_value']

		self.values = []
		self.orig = []
		self.simulator = None

	def simulate(self):
		self.simulator = self.selectStrategy()
		self.values, self.orig = self.simulator.simulate()
		return self.values, self.orig

	def selectStrategy(self):
		if self.strategy == "Buy Close, Sell Open":
			return BCSO(self.startingValue, self.ticker, self.timeframe, self.period)
		elif self.strategy == "Flip Last 30 Direction":
			return Flip30(self.startingValue, self.ticker, self.timeframe, self.period)
		elif self.strategy == "RSI Reversal":
			return RSI(self.startingValue, self.ticker, self.timeframe, self.period, self.rsi_window, self.turnaround_days, self.rsi_value)
		else:
			return None
