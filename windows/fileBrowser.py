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

class init(QWidget):
	def __init__(self, connection):
		super().__init__()
		self.connection = connection

		self.connection.fileBrowser = self

		self.cwd = self.getCwd()

		self.files = []

		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.cwd + " - " + self.connection.hostname)
		
		textHolder = QVBoxLayout()

		self.files = self.getFiles()
		newFont = QFont("Times", 8, QFont.Bold) 
		for file in self.files:
			fileLabel = QPushButton(file)
			fileLabel.setFont(newFont)

			textHolder.addWidget(fileLabel)

		textHolder.addStretch(1)

		self.setLayout(textHolder)
		self.resize(600, 800)
		self.show()

	def closeEvent(self, event):
		self.connection.fileBrowser = None
		event.accept()

	def getCwd(self):
		self.connection.conn.send("getCwd".encode("utf8"))
		return self.connection.conn.recv(1024).decode()

	def getFiles(self):
		self.connection.conn.send("getFiles".encode("utf8"))
		string = self.connection.conn.recv(1024).decode()
		files = string.split(",")
		return files
