#!/usr/bin/env python3

import sys
import time

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

mainWindow = None

def main(app):
    mainWindow = MainWindow()
    mainWindow.move(0, 0)
    mainWindow.show()

    return app.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ret = main(app)

    sys.exit(ret)
