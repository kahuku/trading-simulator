import signal
import sys
import numpy as np
import pyqtgraph

from config import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *

from simulator import Simulator

# TODO: INPUT VALIDATION

class SimulatorGUI(QMainWindow):

	def __init__(self):
		super(SimulatorGUI, self).__init__()
		self.initUI()

	def initUI(self):
		# basic window attributes
		self.setWindowTitle("Trading Simulator")
		# self.setWindowIcon( QIcon('icon312.png') )
		font = QFont()
		font.setFamily(font.defaultFamily())
		self.setMinimumSize(600, 400)

		# box layout
		vbox = QVBoxLayout()
		boxwidget = QWidget()
		boxwidget.setLayout(vbox)
		self.setCentralWidget(boxwidget)

		# pyplot
		h = QHBoxLayout()
		self.plotWidget = pyqtgraph.plot()
		h.addWidget(self.plotWidget)
		vbox.addLayout(h)

		# top row
		h = QHBoxLayout()
		self.startingValueLabel = QLabel("Starting Value: ")
		h.addWidget(self.startingValueLabel)
		self.startingValue = QLineEdit('1000')
		h.addWidget(self.startingValue)
		self.endingValueLabel = QLabel("Ending Value: ")
		h.addWidget(self.endingValueLabel)
		self.endingValue = QLineEdit('1000')
		self.endingValue.setEnabled(False)
		h.addWidget(self.endingValue)
		self.returnLabel = QLabel("% Return: ")
		h.addWidget(self.returnLabel)
		self.returnValue = QLineEdit('0%')
		self.returnValue.setEnabled(False)
		h.addWidget(self.returnValue)
		vbox.addLayout(h)

		# middle row
		h = QHBoxLayout()
		self.tickerLabel = QLabel("Ticker: ")
		h.addWidget(self.tickerLabel)
		self.ticker = QLineEdit("AAPL")
		h.addWidget(self.ticker)
		self.timeFrameLabel = QLabel("Time Frame: ")
		h.addWidget(self.timeFrameLabel)
		self.timeFrameValue = QLineEdit("10")
		h.addWidget(self.timeFrameValue)
		vbox.addLayout(h)

		# bottom row
		h = QHBoxLayout()
		self.strategyLabel = QLabel("Strategy: ")
		h.addWidget(self.strategyLabel)
		self.strategy = QComboBox()
		self.strategy.addItems(["Buy Close, Sell Open", "Flip Last 30 Direction"])
		h.addWidget(self.strategy)
		self.filler = QLabel('')
		h.addWidget(self.filler)
		h.addWidget(self.filler)
		self.timeFrameDay = QRadioButton("D")
		self.timeFrameDay.setChecked(True)
		self.timeFrameMonth = QRadioButton("M")
		self.timeFrameYear = QRadioButton("Y")
		h.addWidget(self.timeFrameDay)
		h.addWidget(self.timeFrameMonth)
		h.addWidget(self.timeFrameYear)
		vbox.addLayout(h)

		# buttons
		h = QHBoxLayout()
		self.processButton = QPushButton('Process')
		self.processButton.clicked.connect(self.processClicked)
		h.addWidget(self.processButton)
		self.clearButton = QPushButton('Clear')
		self.clearButton.clicked.connect(self.clearClicked)
		h.addWidget(self.clearButton)
		h.addStretch(1)
		vbox.addLayout(h)

		# show GUI
		self.show()

	def processClicked(self):
		print("Process clicked")
		self.clearPlot()

		if self.timeFrameDay.isChecked():
			period = "day"
		elif self.timeFrameMonth.isChecked():
			period = "month"
		elif self.timeFrameYear.isChecked():
			period = "year"

		# if not period or not self.timeFrameValue.text() \
		# 	or not self.ticker.text() or self.startingValue.text():
		# 	return

		params = {
			'strategy': self.strategy.currentText(),
			'timeframe': int(self.timeFrameValue.text()),
			'period': period,
			'ticker': self.ticker.text(),
			'startingValue': int(self.startingValue.text())
		}

		self.simulator = Simulator(params)
		self.values, self.originalValues = self.simulator.simulate()

		self.percentChange = (self.values[-1] - self.values[0]) / self.values[0] * 100

		self.endingValue.setText("${:,.2f}".format(self.values[-1]))
		self.returnValue.setText("{:+,.2f}%".format(self.percentChange))

		self.plotValues()

	def clearClicked(self):
		self.startingValue.setText('')
		self.endingValue.setText('')
		self.returnValue.setText('')
		self.ticker.setText('')
		self.timeFrameValue.setText('')
		self.timeFrameDay.setChecked(True)
		self.timeFrameMonth.setChecked(False)
		self.timeFrameYear.setChecked(False)

		self.clearPlot()

	def plotValues(self):
		self.strategyLine = self.plotWidget.plot(np.linspace(0, len(self.values), len(self.values)).tolist(), self.values,
												 pen=pyqtgraph.mkPen('b', width=1))
		self.regularLine = self.plotWidget.plot(np.linspace(0, len(self.originalValues), len(self.originalValues)).tolist(), self.originalValues,
												pen=pyqtgraph.mkPen('w', width=1))

	def clearPlot(self):
		self.plotWidget.clear()

if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = SimulatorGUI()
	sys.exit(app.exec())
