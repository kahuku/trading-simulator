from Simulators.BCSO import BCSO

class Simulator:
	def __init__(self, params):
		super().__init__()

		self.strategy = params['strategy']
		self.timeframe = params['timeframe']
		self.period = params['period']
		self.ticker = params['ticker']
		self.startingValue = params['startingValue']
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
		else:
			return None