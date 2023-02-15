from PySide6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow

app = QApplication(sys.argv)
mainwindow = MainWindow()

mainwindow.show()
app.exec()
