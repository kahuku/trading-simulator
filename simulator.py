from Simulators.BCSO import BCSO

class Simulator:
	def __init__(self, params):
		super().__init__()

		self.strategy = params['strategy']
		self.timeframe = params['timeframe']
		self.period = params['period']
		self.ticker = params['ticker']
		self.startingValue = params['startingValue']

		self.simulate()

	def simulate(self):
		self.strategyClass = self.selectStrategy()

	def selectStrategy(self):
		if self.strategy == "Buy Close, Sell Open":
			return BCSO()