from Ms import MS
from scipy.io import loadmat
from PySide6.QtWidgets import QApplication
import sys
import numpy as np
app = QApplication(sys.argv)

ms_file = loadmat("ms.mat",struct_as_record=False)["ms"]
ms_file = ms_file[0,0]
ms = MS(ms_file)
import pyqtgraph as pg
g = pg.plot()
g.setXRange(0,500)
g.setYRange(0,500)
iso = pg.IsocurveItem(ms.NeuronList[0].ROI, level = 1)
g.addItem(iso)
# x=np.arange(10)
# y1=np.sin(x)

# bg1 = pg.BarGraphItem(x=x, height=y1, width=0.3,brush='r')
# g.addItem(bg1)
app.exec()
