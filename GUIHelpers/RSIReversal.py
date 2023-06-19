from config import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *

class RSIInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RSI Reversal")
        layout = QFormLayout()
        self.rsi_window_input = QLineEdit('14')
        self.turnaround_days_input = QLineEdit()
        self.rsi_value_input = QLineEdit('30')
        layout.addRow(QLabel("RSI Rolling Average Window:"), self.rsi_window_input)
        layout.addRow(QLabel("Turnaround Days:"), self.turnaround_days_input)
        layout.addRow(QLabel("RSI Value:"), self.rsi_value_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.turnaround_days_input.setFocus()

    def get_values(self):
        rsi_window = int(self.rsi_window_input.text()) if self.rsi_window_input.text().isdigit() else 0
        turnaround_days = int(self.turnaround_days_input.text()) if self.turnaround_days_input.text().isdigit() else 0
        rsi_value = int(self.rsi_value_input.text()) if self.rsi_value_input.text().isdigit() else 0
        return rsi_window, turnaround_days, rsi_value
