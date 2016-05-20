#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets
from gui import ImageQueryWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImageQuery = ImageQueryWindow()
    ImageQuery.show()
    sys.exit(app.exec_())
