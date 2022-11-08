import signal
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from config import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *

from simulator import Simulator

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
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		h.addWidget(self.canvas)
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
		self.strategy.addItems(["Buy Close, Sell Open"])
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

		if self.timeFrameDay.isChecked():
			period = "day"
		elif self.timeFrameMonth.isChecked():
			period = "month"
		elif self.timeFrameYear.isChecked():
			period = "year"

		params = {
			'strategy': self.strategy.currentText(),
			'timeframe': int(self.timeFrameValue.text()),
			'period': period,
			'ticker': self.ticker.text(),
			'startingValue': int(self.startingValue.text())
		}
		simulator = Simulator(params)

	def clearClicked(self):
		self.startingValue.setText('')
		self.endingValue.setText('')
		self.returnValue.setText('')
		self.ticker.setText('')
		self.timeFrameValue.setText('')

if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = SimulatorGUI()
	sys.exit(app.exec())
