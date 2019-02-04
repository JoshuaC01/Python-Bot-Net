#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import sip
from PyQt5.QtCore import QThread, pyqtSignal
import extra, masterHelper
import threading, time
from functools import partial
import select

from windows import shell
from windows import fileBrowser

class init(QWidget):
	def __init__(self, connection):
		super().__init__()
		self.connection = connection

		self.connection.configOpen = True
		self.connection.config = self

		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.connection.hostname + " - Config Panel")
		grid = QGridLayout()

		self.hostNameLabel = QLabel("Hostname: ")

		grid.addWidget(self.hostNameLabel, 0, 0)

		self.hostNameEdit = QLineEdit(self.connection.hostname)
		self.hostNameEdit.returnPressed.connect(self.changeHostname)
		grid.addWidget(self.hostNameEdit, 0, 1)



		self.OSLabel = QLabel("OS: ")

		grid.addWidget(self.OSLabel, 1, 0)

		self.OSEdit = QLineEdit(self.connection.os)
		self.OSEdit.returnPressed.connect(self.changeOS)
		grid.addWidget(self.OSEdit, 1, 1)

		self.shellBtn = QPushButton("Shell")
		self.shellBtn.clicked.connect(partial(self.shellClient, self.connection))

		grid.addWidget(self.shellBtn, 2, 0)

		self.fileBtn = QPushButton("Broswe Files")
		self.fileBtn.clicked.connect(partial(self.fileBrowser, self.connection))

		grid.addWidget(self.fileBtn, 2, 1)

		self.setLayout(grid)
		self.resize(600, 100)
		self.show()

	def closeEvent(self, event):
		self.connection.configOpen = False
		self.connection.config = None
		self.changeHostname()
		self.changeOS()
		event.accept()

	def changeHostname(self):
		self.connection.hostname = self.hostNameEdit.text()
		self.setWindowTitle(self.connection.hostname + " - Config Panel")

	def changeOS(self):
		self.connection.os = self.OSEdit.text()

	def shellClient(self, connection):
		tempShell = shell.init(connection)

	def fileBrowser(self, connection):
		tempBrowser = fileBrowser.init(connection)
