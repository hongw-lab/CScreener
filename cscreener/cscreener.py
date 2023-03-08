from PySide6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    app.installEventFilter(mainwindow)
    app.setApplicationName("CScreener")
    mainwindow.show()
    app.aboutToQuit.connect(mainwindow.stop_threads)

    app.exec()


if __name__ == "__main__":
    main()
