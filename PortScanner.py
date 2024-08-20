from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, date

import sys
import socket
import time
import datetime

class PortScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.background = "708090"
        self.color = "#FFFF33"

        self.createMenus()
        self.initUI()
        
        self.setWindowTitle("PortScanner")
        self.setGeometry(360, 170, 1200, 800)
        #dself.setStyleSheet(f"background-color:{self.background}")
        
    def initUI(self):

        targetLayout = QGridLayout()
        targetLayout.setSpacing(20)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegExp = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "\\/" + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegExp, self)
        
        targetLabel = QLabel("IP address:")
        targetLabel.setFont(QFont("Times", 15))
        targetLabel.setStyleSheet(f"color: {self.color};")
        targetLabel.setAlignment(Qt.AlignLeft)
        
        self.targetEdit = QLineEdit()
        self.targetEdit.setStyleSheet(f"background-color: white; color: black;")
        self.targetEdit.setValidator(ipValidator)
        self.targetEdit.setPlaceholderText("Example: 8.8.8.8")
        self.targetEdit.setMaximumWidth(200)

        portRange = "([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-6][0-9][0-9][0-9][0-9])"
        portRegExp = QRegExp("^" + portRange + "-" + portRange + "$")
        portValidator = QRegExpValidator(portRegExp, self)
        
        targetPortLabel = QLabel("Ports:")
        targetPortLabel.setFont(QFont("Times", 15))
        targetPortLabel.setStyleSheet(f"color: {self.color};")

        self.targetPortEdit = QLineEdit()
        self.targetPortEdit.setStyleSheet("background-color: white; color: black;")
        self.targetPortEdit.setValidator(portValidator)
        self.targetPortEdit.setPlaceholderText("Example: 1-1024 or 22")
        self.targetPortEdit.setMaximumWidth(200)

        targetVLayout = QGridLayout()
        targetVLayout.addWidget(targetLabel, 0, 0)
        targetVLayout.addWidget(self.targetEdit, 0, 1, 1, 2)
        targetVLayout.addWidget(targetPortLabel, 1, 0)
        targetVLayout.addWidget(self.targetPortEdit, 1, 1, 1, 2)

        targetFrame = QFrame()
        targetFrame.setFrameShape(QFrame.Box)
        targetFrame.setFrameShadow(QFrame.Raised)
        targetFrame.setLineWidth(3)
        targetFrame.setStyleSheet(f"color: {self.color}; border: 2px solid {self.color}; border-radius: 5px;")
        targetFrame.setLayout(targetVLayout)

        targetLayout.addWidget(targetFrame, 0, 0, 1, 2)

        optionsLayout = QGridLayout()

        timerLabel = QLabel("Timer")
        timerLabel.setFont(QFont("Times", 15))
        timerLabel.setStyleSheet(f"color: {self.color}")

        self.timerBox = QSpinBox()
        self.timerBox.setRange(5, 60)
        self.timerBox.setSingleStep(1)

        optionsVLayout = QGridLayout()
        optionsVLayout.addWidget(timerLabel, 0, 0, 1, 1)
        optionsVLayout.addWidget(self.timerBox, 0, 1, 1, 1)

        optionsFrame = QFrame()
        optionsFrame.setFrameShape(QFrame.Box)
        optionsFrame.setFrameShadow(QFrame.Raised)
        optionsFrame.setLineWidth(3)
        optionsFrame.setStyleSheet(f"color: {self.color}; border: 2px solid {self.color}; border-radius: 5px;")
        optionsFrame.setLayout(optionsVLayout)

        optionsLayout.addWidget(optionsFrame, 0, 0, 1, 2)

        saveButton = QPushButton("Save to file")
        saveButton.setFont(QFont("Times", 15))
        saveButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color}")
        saveButton.clicked.connect(self.saveToFile)

        scanningButton = QPushButton("Start scanning")
        scanningButton.setFont(QFont("Times", 15))
        scanningButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color};")
        scanningButton.clicked.connect(self.startScanning)

        exitButton = QPushButton("Exit")
        exitButton.setFont(QFont("Times", 15))
        exitButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color}")
        exitButton.clicked.connect(self.exitApp)

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setStyleSheet("background-color:white; color: black;")

        mainLayout = QGridLayout()
        
        mainLayout.addLayout(targetLayout, 0, 1, 1, 2)  
        mainLayout.addLayout(optionsLayout, 0, 3, 1, 2)   
        mainLayout.addWidget(saveButton, 1, 0, 1, 1)
        mainLayout.addWidget(scanningButton, 1, 2, 1, 2)
        mainLayout.addWidget(exitButton, 1, 5, 1, 1)
        mainLayout.addWidget(self.outputText, 2, 0, 1, 6)
        
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

    def saveToFile(self):
        filename, _ =QFileDialog.getSaveFileName(self, "Save file", "./", "Text file(*.txt);;All files(*.*)")
        
        if filename:
            with open(filename, "w") as file:
                file.write(f"IP address: {self.targetEdit.text()}\n")
                file.write(f"Ports: {self.targetPortEdit.text()}\n")
                file.write(f"Timer: {self.timerBox.value()}\n")
                file.write(f"Scanning starts at {datetime.datetime.now()}")
        
    def startScanning(self):
        self.outputText.clear()
        self.outputText.append(f"<h4><b>IP address:</b> {self.targetEdit.text()}</h4>")
        self.outputText.append(f"<h4><b>Ports:</b> {self.targetPortEdit.text()}</h4>")
        self.outputText.append(f"<h4><b>Timer:</b> {self.timerBox.value()}</h4>")
        self.outputText.append(f"<h4><b>Scanning starts at {datetime.datetime.now()}</b></h4> \n")

        self.PortScanner()
        
    def exitApp(self):
        exitBox = QMessageBox()
        exitBox.setWindowTitle("Exit")
        exitBox.setText("Are you really want to exit the application?")
        exitBox.setGeometry(750, 450, 400, 300)
        exitBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exitBox.setDefaultButton(QMessageBox.Yes)
        
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
                    time.sleep(self.timer)
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
        target_ips = self.targetEdit.text()
        target_ports = self.targetPortEdit.text()
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

