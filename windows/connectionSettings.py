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

		self.commandEntry = QPushButton("Test Setting")
		grid.addWidget(self.commandEntry, 0, 0)

		self.setLayout(grid)
		self.resize(600, 500)
		self.show()

	def closeEvent(self, event):
		self.connection.configOpen = False
		self.connection.config = None
		event.accept()