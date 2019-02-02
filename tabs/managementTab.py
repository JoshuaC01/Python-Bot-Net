#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import sip
from PyQt5.QtCore import QThread, pyqtSignal
import extra, masterHelper
import threading, time
from functools import partial

class logPanel(QGroupBox):
	def __init__(self, mainLayout):
		super().__init__("Log")
		self.mainLayout = mainLayout
		self.initUI()

	def initUI(self):
		vBox = QVBoxLayout()

		self.logText = QTextEdit()
		self.logText.setReadOnly(True)
		self.log("Testing Logging Feature")

		vBox.addWidget(self.logText)
		self.setLayout(vBox)

	def log(self, text):
		self.logText.setText(self.logText.toPlainText() + text + "\n")

class settingsPanel(QGroupBox):
	def __init__(self, mainLayout):
		super().__init__("Settings")
		self.mainLayout = mainLayout
		self.initUI()

	def initUI(self):
		vBox = QVBoxLayout()

		clearButton = QPushButton("Force Refresh")
		clearButton.clicked.connect(self.mainLayout.clearPorts)

		#vBox.addWidget(refreshButton)
		vBox.addWidget(clearButton)
		vBox.addStretch(1)
		self.setLayout(vBox)




class portScanner(QThread):

	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self, ports):
		QThread.__init__(self)
		self.allConns = ports

	def __del__(self):
		self.wait()

	def run(self):
		print("Starting Scan")
		while True:
			self.data = masterHelper.updateConns(self.allConns)
			self.allConns = self.data[0]
			self.signal.emit(self.data)
			time.sleep(1)

class init(QWidget):
	def __init__(self, mainWindow):
		super().__init__()

		self.mainWindow = mainWindow

		availableConns = []
		for i in range(len(self.mainWindow.availablePorts)):
			availableConns.append(extra.NewConnection(self.mainWindow.availablePorts[i]))

		self.allConns = availableConns

		

		self.initUI()

		self.startPortScanner()

	def startPortScanner(self):
		self.scanThread = portScanner(self.allConns)
		self.scanThread.signal.connect(self.handleScannerOutput)
		self.scanThread.start()

	def handleScannerOutput(self, output):
		self.refreshPorts(output[0])
		for connection in output[1]:
			self.logPanel.log("Recieved connection from: " + connection.hostname + "(" + connection.os + ") - " + str(connection.port))

		for connection in output[2]:
			self.logPanel.log("Lost connection from: " + connection.hostname + "(" + connection.os + ") - " + str(connection.port))

	def initUI(self):
		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.setLayout(self.grid)

		self.portList = self.makePortBox()

		self.settingsPanel = settingsPanel(self)

		self.logPanel = logPanel(self)

		#self.currentPortsPanel = currentPortsPanel(self)

		self.grid.addWidget(self.portList, 0, 1, 2, 1)
		self.grid.addWidget(self.settingsPanel, 0, 2, 1, 1)
		#self.grid.addWidget(self.currentPortsPanel, 1, 2, 1, 1)
		self.grid.addWidget(self.logPanel, 0, 3, 2, 2)

		#self.refreshPorts()

		self.resize(1920, 1080)
		self.setWindowTitle('CFD - Botnet Manager')  
		self.show()

	def makePortBox(self):
		vBox = QVBoxLayout()
		groupBox = QGroupBox("Connections:")

		groupBox.setLayout(vBox)

		return groupBox

	def refreshPorts(self, allConns):
		self.allConns = allConns
		vBox = QVBoxLayout()
		for connection in self.allConns:
			if(not connection.active):
				continue
			portLabel = QLabel(connection.hostname + "(" + connection.os + ") - " + str(connection.port))
			#portConnect = QPushButton("Connect")
			portDisconnect = QPushButton("Disconnect")
			portDisconnect.clicked.connect(partial(self.disconnectClient, connection))

			hBox = QHBoxLayout()
			hBox.addWidget(portLabel)
			#hBox.addWidget(portConnect)
			hBox.addWidget(portDisconnect)
				
			vBox.addLayout(hBox)
		vBox.addStretch(1)

		self.deleteLayout(self.portList.layout())

		self.portList.setLayout(vBox)


	def disconnectClient(self, connection):
		connection.conn.send("disconnect".encode("utf8"))
		self.logPanel.log("Disconnect: " + connection.hostname + ", At Port: " + str(connection.port))

	def clearPorts(self):
		vBox = QVBoxLayout()
		groupBox = QGroupBox("Connections:")
		vBox.addStretch(1)

		groupBox.setLayout(vBox)

		self.deleteLayout(self.portList.layout())

		self.portList.setLayout(vBox)

	def deleteLayout(self, cur_lay):
		if cur_lay is not None:
			while cur_lay.count():
				item = cur_lay.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.deleteLayout(item.layout())

			sip.delete(cur_lay)