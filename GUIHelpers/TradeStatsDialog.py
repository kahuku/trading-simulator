import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from config import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import *
    import pyqtgraph

class TradeStatsDialog(QDialog):
    def __init__(self, profitable_trades, unprofitable_trades, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Trade Statistics")
        self.setMinimumSize(800, 600)
        self.profitable_trades = profitable_trades
        self.unprofitable_trades = unprofitable_trades

        layout = QVBoxLayout(self)

        # Create histogram
        fig, ax = plt.subplots(figsize=(8, 6))
        bins = [0, 1, 2]
        labels = ['Profitable', 'Unprofitable']
        colors = ['green', 'red']

        # Plot the histogram columns
        ax.bar(labels, [profitable_trades, unprofitable_trades], color=colors)

        # Set labels and title
        ax.set_xlabel("Trade Result")
        ax.set_ylabel("Frequency")
        ax.set_title("Trade Profitability")

        # Add text above each column indicating the count
        for i, v in enumerate([profitable_trades, unprofitable_trades]):
            ax.text(i, v + 1, str(v), ha='center', fontweight='bold')

        # Add the plot to the layout
        layout.addWidget(FigureCanvas(fig))
        layout.addWidget(NavigationToolbar2QT(fig.canvas, self))

    def getProfitableTrades(trades):
        profitable_trades = sum(trades[i] > trades[i - 1] for i in range(1, len(trades)))
        unprofitable_trades = sum(trades[i] < trades[i - 1] for i in range(1, len(trades)))
        return profitable_trades, unprofitable_trades
