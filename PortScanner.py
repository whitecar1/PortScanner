from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, date

import sys
import socket

class PortScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.background = "708090"
        self.color = "#FFFF33"
        self.targetIp = None
        self.minTargetPort = None
        self.maxTargetPort = None
        
        self.createMenus()
        self.initUI()
        
        self.setWindowTitle("PortScanner")
        self.setGeometry(360, 170, 1200, 800)
        self.setStyleSheet(f"background-color:{self.background}")
        
    def initUI(self):
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegExp = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegExp, self)

        targetLayout = QHBoxLayout()
        targetLayout.setSpacing(20)
        
        targetLabel = QLabel("IP(s) range:")
        targetLabel.setFont(QFont("Arial", 15))
        targetLabel.setStyleSheet(f"color: {self.color}")
        targetLabel.setAlignment(Qt.AlignLeft)
        
        self.targetEdit = QLineEdit()
        self.targetEdit.setStyleSheet("background-color: white; color: red;")
        self.targetEdit.setValidator(ipValidator)
        self.targetEdit.setMaximumWidth(150)
        #self.targetEdit.setAlignment(Qt.AlignCenter)
        
        toLabel = QLabel("to")
        toLabel.setFont(QFont("Arial", 15))
        toLabel.setStyleSheet(f"color: {self.color}")
        toLabel.setAlignment(Qt.AlignLeft)

        self.targetTwoEdit = QLineEdit()
        self.targetTwoEdit.setStyleSheet("background-color: white; color: red;")
        self.targetTwoEdit.setValidator(ipValidator)
        self.targetTwoEdit.setMaximumWidth(150)
        self.targetTwoEdit.setAlignment(Qt.AlignLeft)

        orLabel = QLabel("or    /")
        orLabel.setFont(QFont("Arial", 15))
        orLabel.setStyleSheet(f"color: {self.color}")
        orLabel.setAlignment(Qt.AlignCenter)
        orLabel.setAlignment(Qt.AlignLeft)

        self.cidrEdit = QLineEdit()
        self.cidrEdit.setStyleSheet("background-color: white; color: red;")
        self.cidrEdit.setValidator(ipValidator)
        self.cidrEdit.setMaximumWidth(30)
        self.cidrEdit.setAlignment(Qt.AlignLeft)
        
        targetLayout.addWidget(targetLabel)
        targetLayout.addWidget(self.targetEdit)
        targetLayout.addWidget(toLabel)
        targetLayout.addWidget(self.targetTwoEdit)
        targetLayout.addWidget(orLabel)
        targetLayout.addWidget(self.cidrEdit)

        portRange = "([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-6][0-9][0-9][0-9][0-9])"
        portRegExp = QRegExp("^" + portRange + "$")
        portValidator = QRegExpValidator(portRegExp, self)
        
        targetPortLabel = QLabel("Target port(s):")
        targetPortLabel.setFont(QFont("Arial", 15))
        targetPortLabel.setStyleSheet(f"color: {self.color}")

        self.targetPortEdit = QLineEdit()
        self.targetPortEdit.setStyleSheet("background-color: white; color: red;")
        self.targetPortEdit.setValidator(portValidator)

        self.targetPortEdit = QLineEdit()
        self.targetPortEdit.setStyleSheet("background-color: white; color: red;")
        self.targetPortEdit.setValidator(portValidator)

        saveButton = QPushButton("Save to file")
        saveButton.setFont(QFont("Arial", 15))
        saveButton.setStyleSheet("background-color: #CC0000; color: #FFD700;")
        saveButton.clicked.connect(self.saveToFile)
        
        scanningButton = QPushButton("Start scanning")
        scanningButton.setFont(QFont("Arial", 15))
        scanningButton.setStyleSheet("background-color: #FF00FF; color: #FFD700;")
        scanningButton.clicked.connect(self.startScanning)

        exitButton = QPushButton("Exit")
        exitButton.setFont(QFont("Arial", 15))
        exitButton.setStyleSheet("background-color: #CC0000; color: #FFD700;")
        exitButton.clicked.connect(self.exitApp)

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setStyleSheet("background-color:white; color: black;")

        mainLayout = QGridLayout()
        mainLayout.addLayout(targetLayout, 0, 0)
        '''
        mainLayout.addWidget(targetLabel, 0, 0)
        mainLayout.addWidget(self.targetEdit, 0, 1)
        mainLayout.addWidget(toLabel, 0, 2)
        mainLayout.addWidget(self.targetTwoEdit, 0, 3)
        mainLayout.addWidget(targetPortLabel, 1, 0)
        mainLayout.addWidget(self.targetPortEdit, 1, 1)
        mainLayout.addWidget(saveButton, 3, 0)
        mainLayout.addWidget(scanningButton, 3, 1)
        mainLayout.addWidget(exitButton, 3, 2)
        mainLayout.addWidget(self.outputText, 4, 0, 1, 3)
        '''
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def createMenus(self):
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet("color: red; background-color: #FFFFFF")
        fileMenu = mainMenu.addMenu("File")
        settingsMenu = mainMenu.addMenu("Settings")
        helpMenu = mainMenu.addMenu("Help")
        aboutMenu = mainMenu.addMenu("About")
            
    def TargetIpChanged(self):       
        self.targetIP = self.targetEdit.text()
        if self.targetIP == "":
            return "127.0.0.1"
        return self.targetIP
        
    def TargetPortChanged(self):
        self.targetPort = self.targetPortEdit.text()
        if self.targetPort == "":
            return "1-1024"
        elif self.targetPort == "*":
            return "1-65535"
        return self.targetPort
        
    def TargetOsChanged(self):
        return "not defined"
    
    def saveToFile(self):
        filename, _ =QFileDialog.getSaveFileName(self, "Save file", "./", "Text file(*.txt);;All files(*.*)")
        
        if filename:
            with open(filename, "w") as file:
                #file.write(self.tabs)
                pass
        
    def startScanning(self):
        self.outputText.clear()
        self.outputText.append("Start scanning...\n")

        self.PortScanner()
        
    def exitApp(self):
        exitBox = QMessageBox()
        exitBox.setWindowTitle("Exit")
        exitBox.setText("Are you really want to exit the application?")
        exitBox.setGeometry(750, 450, 400, 300)
        exitBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exitBox.setDefaultButton(QMessageBox.No)
        
        result = exitBox.exec_()
        if result == QMessageBox.Yes:
            sys.exit(0)

    def ScanPort(self, target:str, ports:str):

        if "-" in ports:
            ports = ports.split("-")
            for port in range(int(ports[0]), int(ports[1])+1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target, port))
                    self.outputText.append(f"{port}     open")
                    sock.close()
                except:
                    pass
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, int(ports)))
                self.outputText.append(f"{ports}        open")
                sock.close()
            except:
                pass
        
    def PortScanner(self):
        target_ips = self.TargetIpChanged()
        target_ports = self.TargetPortChanged()
        for target in target_ips.split(","):
            try:
                self.ScanPort(target, target_ports)
            except:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = PortScanner()
    scanner.show()
    sys.exit(app.exec_())