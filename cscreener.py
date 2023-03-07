from PySide6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow

app = QApplication(sys.argv)
mainwindow = MainWindow()
app.installEventFilter(mainwindow)
mainwindow.show()
app.aboutToQuit.connect(mainwindow.stop_threads)
app.exec()




