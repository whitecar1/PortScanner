from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
import socket
import colored

class Settings(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
        self.setWindowTitle("Settings")
        self.setGeometry(400, 200, 600, 700)
        #self.setStyleSheet(f"background-color: {background}")
        
    def initUI(self):
        backgroundLabel = QLabel("Change background color:")
        backgroundLabel.setFont(QFont("Arial", 15))
        #backgroundLabel.setStyleSheet(f"color: {color}")
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(backgroundLabel, 0, 0)
        
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
