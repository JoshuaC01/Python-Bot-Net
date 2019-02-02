
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import sip
from PyQt5.QtCore import QThread, pyqtSignal
import extra, masterHelper
import threading, time
from functools import partial

# -- MASTER SCRIPT -- #
import master
import extra

class currentPortsPanel(QGroupBox):
	def __init__(self, mainLayout):
		super().__init__("Listening On Ports")
		self.mainLayout = mainLayout
		self.initUI()

	def initUI(self):

		self.updatePorts()
		#vBox.addWidget(refreshButton)

	def updatePorts(self):
		vBox = QVBoxLayout()
		removeAllButton = QPushButton("Remove All Ports")
		removeAllButton.clicked.connect(self.removeAllPorts)
		vBox.addWidget(removeAllButton)
		for port in self.mainLayout.mainWindow.availablePorts:
			hBox = QHBoxLayout()

			text = QLabel(str(port))
			removeButton = QPushButton("Remove")
			removeButton.clicked.connect(partial(self.removePort, port))

			hBox.addWidget(text)
			hBox.addWidget(removeButton)
			hBox.addStretch(1)

			vBox.addLayout(hBox)

		vBox.addStretch(0.6)

		self.mainLayout.deleteLayout(self.layout())
		self.setLayout(vBox)

	def removePort(self, port):
		for connection in self.mainLayout.mainWindow.allConns:
			if connection.port == port and connection.active == False:
				self.mainLayout.mainWindow.availablePorts.remove(port)
				self.mainLayout.mainWindow.allConns.remove(connection)
				self.mainLayout.mainWindow.logPanel.log("Removed Port: " + str(port))

		self.updatePorts()

	def addPort(self, port):
		if port not in self.mainLayout.mainWindow.availablePorts:
			self.mainLayout.mainWindow.availablePorts.append(port)
			self.mainLayout.mainWindow.allConns.append(extra.NewConnection(port))
			self.updatePorts()
			self.mainLayout.mainWindow.logPanel.log("Added Port: " + str(port))

	def removeAllPorts(self):
		for port in self.mainLayout.mainWindow.availablePorts:
			self.removePort(port)

class addPortPanel(QGroupBox):
	def __init__(self, mainLayout):
		super().__init__("Listening On Ports")
		self.mainLayout = mainLayout
		self.initUI()

	def initUI(self):
		self.addPortBox = QLineEdit()

		vBox = QVBoxLayout()
		vBox.addStretch(1)

		hBox = QHBoxLayout()

		hBox.addWidget(self.addPortBox)

		addButton = QPushButton("Add Port")
		addButton.clicked.connect(self.addPortData)

		hBox.addWidget(addButton)

		vBox.addLayout(hBox)
		
		self.setLayout(vBox)

	def addPortData(self):
		try:
			port = int(self.addPortBox.text())
			self.addPortBox.setText("")
			self.mainLayout.currentPortsPanel.addPort(port)
		except Exception as e:
			print(e)
			self.addPortBox.setText("")

class init(QWidget):
	def __init__(self, mainWindow):
		super().__init__()

		self.mainWindow = mainWindow

		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		#self.grid.setSpacing(10)

		self.addPort = addPortPanel(self)

		self.currentPortsPanel = currentPortsPanel(self)

		self.grid.addWidget(self.addPort, 1, 0)
		self.grid.addWidget(self.currentPortsPanel, 0, 0)
		#self.grid.addWidget(self.mainWindow.logPanel,0, 1, 2, 5)

		self.setLayout(self.grid)

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