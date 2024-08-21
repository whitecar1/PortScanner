from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import time
import socket
import datetime

import interface

class PortScanner(QMainWindow):
    def __init__(self):
        super().__init__()

    def ScanPort(self, target:str, ports:str, results):
        if "-" in ports:
            ports = ports.split("-")
            for port in range(int(ports[0]), int(ports[1])+1):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target, port))
                    service = socket.getservbyport(port)
                    results[port] = ["open", service]
                    sock.close()
                    #time.sleep(timer)
                except:
                    pass
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, int(ports)))
                service = socket.getservbyport(int(ports))
                results[int(ports)] = ["open", service]
                sock.close()
            except:
                pass
        
    def PortScanner(self):
        results = {}
        
        target_ips, target_ports, _ =  interface.PortScannerInterFace.target()
        for target in target_ips.split(","):
            try:
                self.ScanPort(target, target_ports)
            except:
                pass
            
        return results
