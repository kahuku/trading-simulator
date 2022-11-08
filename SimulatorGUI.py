import signal
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from config import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *

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

		# buttons
		h = QHBoxLayout()
		self.processButton = QPushButton('Process')
		self.clearButton = QPushButton('Clear')
		h.addWidget(self.processButton)
		h.addWidget(self.clearButton)
		h.addStretch(1)
		vbox.addLayout(h)

		# show GUI
		self.show()

if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = SimulatorGUI()
	sys.exit(app.exec())