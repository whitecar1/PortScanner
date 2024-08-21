from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import time
import socket
import datetime

import scanner
import interface

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = interface.PortScannerInterFace()
    scanner.show()
    sys.exit(app.exec_())

