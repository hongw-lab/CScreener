import sys
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from data import Neuron
from PySide6.QtCore import Qt
import numpy as np
class CustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, items: Optional[list] = None,
        properties: Optional[List[str]] = None):
        super().__init__(*args, **kwargs)
        self.neuron = neuron
    def data(self, role):
        if role == Qt.DisplayRole:
            return str(self.neuron.ID)
        else:
            return super().data(role)

app = QApplication(sys.argv)

table = QTableWidget(2, 2)
neuron = Neuron(ID=1,FiltTrace=np.zeros((2,2)),RawTrace=np.zeros((2,2)),Spike=np.zeros((2,2)),ROI=np.zeros((2,2)),Label=1)
neuronItem = CustomTableWidgetItem(neuron=neuron)
table.setItem(0, 0, neuronItem)

table.show()

sys.exit(app.exec())
