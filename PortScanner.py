from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, date

import sys
import socket
import colored


class PortScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.background = "#000066"
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
        targetLabel = QLabel("Target IP:")
        targetLabel.setFont(QFont("Arial", 15))
        targetLabel.setStyleSheet(f"color: {self.color}")
        
        self.targetEdit = QLineEdit()
        self.targetEdit.setStyleSheet("background-color: white; color: red;")
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegExp = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegExp, self)
        self.targetEdit.setValidator(ipValidator)
        
        portRange = "([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-5][0-9][0-9][0-9][0-9])"
        portRegExp = QRegExp("^" + portRange + "\\-" + portRange + "$")
        portValidator = QRegExpValidator(portRegExp, self)
        
        minPortLabel = QLabel("Minimal port:")
        minPortLabel.setFont(QFont("Arial", 15))
        minPortLabel.setStyleSheet(f"color: {self.color}")

        self.minPortEdit = QLineEdit()
        self.minPortEdit.setStyleSheet("background-color: white; color: red;")
        self.minPortEdit.setValidator(portValidator)
        
        maxPortLabel = QLabel("Maximum port:")
        maxPortLabel.setFont(QFont("Arial", 15))
        maxPortLabel.setStyleSheet(f"color: {self.color}")

        self.maxPortEdit = QLineEdit()
        self.maxPortEdit.setStyleSheet("background-color: white; color: red;")
        self.maxPortEdit.setValidator(portValidator)

        saveButton = QPushButton("Save to file")
        saveButton.setFont(QFont("Arial", 15))
        saveButton.setStyleSheet("background-color: #CC0000; color: #FFD700;")
        saveButton.clicked.connect(self.save_to_file)
        
        scanningButton = QPushButton("Start scanning")
        scanningButton.setFont(QFont("Arial", 15))
        scanningButton.setStyleSheet("background-color: #FF00FF; color: #FFD700;")
        scanningButton.clicked.connect(self.startScanning)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("background-color: #FFFFFF; color: red;")

        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Target Details")
        self.tab1_layout = QGridLayout()
        self.tab1.setLayout(self.tab1_layout)

        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "ScanDetails")
        self.tab2_layout = QGridLayout()
        self.tab2.setLayout(self.tab2_layout)

        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "Results")
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(targetLabel, 0, 0)
        mainLayout.addWidget(self.targetEdit, 0, 1)
        mainLayout.addWidget(minPortLabel, 1, 0)
        mainLayout.addWidget(self.minPortEdit, 1, 1)
        mainLayout.addWidget(maxPortLabel, 2, 0)
        mainLayout.addWidget(self.maxPortEdit, 2, 1)
        mainLayout.addWidget(saveButton, 3, 0)
        mainLayout.addWidget(scanningButton, 3, 1)
        mainLayout.addWidget(self.tabs, 4, 0, 1, 3)
        
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
            
    def validate_ip_adresses(self, targets):
        pass
    
    def TargetIpChanged(self):       
        self.targetIP = self.targetEdit.text()
        if self.targetIP == "":
            return "127.0.0.1"
        return self.targetIP
        
    def TargetPortChanged(self):
        self.minTargetPort = self.minPortEdit.text()
        self.maxTargetPort = self.maxPortEdit.text()
        if self.minTargetPort == "" and self.maxTargetPort == "":
            return "1-1024"
        elif self.minTargetPort == "*" and  (self.maxTargetPort == "" or self.maxTargetPort == "*"):
            print("1-65535")
            return "1-65535"
        elif self.minTargetPort != "" and self.maxTargetPort != "":
            return f"{self.minTargetPort}-{self.maxTargetPort}"
        elif self.minTargetPort != "" and self.maxTargetPort == "":
            return self.minTargetPort
        elif self.minTargetPort == "" and self.maxTargetPort != "":
            return self.maxTargetPort
        
    def TargetOsChanged(self):
        return "not defined"
    
    def save_to_file(self):
        filename, _ =QFileDialog.getSaveFileName(self, "Save file", "./", "Text file(*.txt);;All files(*.*)")
        
        if filename:
            with open(filename, "w") as file:
                #file.write(self.tabs)
                pass
        
    def startScanning(self):
        #self.tabs.clear()

        targetIP = QLabel(f"Target IPs: {self.TargetIpChanged()}")
        targetIP.setFont(QFont("Arial", 15))
        targetIP.setAlignment(Qt.AlignLeft)

        targetPort = QLabel(f"Target Ports: {self.TargetPortChanged()}")
        targetPort.setFont(QFont("Arial", 15))
        targetPort.setAlignment(Qt.AlignLeft)

        targetOs = QLabel(f"Target OS: {self.TargetOsChanged()}")
        targetOs.setFont(QFont("Arial", 15))
        targetOs.setAlignment(Qt.AlignLeft)

        self.tab1_layout.addWidget(targetIP, 0, 0)
        self.tab1_layout.addWidget(targetPort, 1, 0)
        self.tab1_layout.addWidget(targetOs, 2, 0)

        now = datetime.now().strftime("%H:%M:%S")
        today = date.today()

        timeLabel = QLabel(f"Scanning begins at {now} {today}")
        timeLabel.setFont(QFont("Arial", 15))
        timeLabel.setAlignment(Qt.AlignLeft)

        self.tab2_layout.addWidget(timeLabel, 0, 0)

        self.PortScanner()
        
    def ScanPort(self, target:str, ports:str):
        startLabel = QLabel("Port     Status")
        startLabel.setAlignment(Qt.AlignLeft)
        startLabel.setFont(QFont("Arial", 15))
        self.tab2_layout.addWidget(startLabel, 1, 0)

        if "-" in ports:
            ports = ports.split("-")
            for port in range(int(ports[0]), int(ports[1])+1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target, port))
                    portLabel = QLabel(f"{port}        open")
                    portLabel.setAlignment(Qt.AlignLeft)
                    portLabel.setFont(QFont("Arial", 15))
                    self.tab2_layout.addWidget(portLabel)
                    sock.close()
                except:
                    pass
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, int(ports)))
                portLabel = QLabel(f"{ports}        open")
                portLabel.setAlignment(Qt.AlignLeft)
                portLabel.setFont(QFont("Arial", 15))
                self.tab2_layout.addWidget(portLabel)
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
    
TEst