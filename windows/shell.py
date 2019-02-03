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

class shellReciever(QThread):

	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self, connection):
		QThread.__init__(self)
		self.connection = connection

	def __del__(self):
		self.wait()

	def run(self):
		try:
			while True:
				print("Listening: ")
				#conn.setTimeout(5)
				text = self.connection.conn.recv(1024).decode()
				print("Recieved")
				self.signal.emit(text)
		except:
			pass

class sendCommand(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self, connection, command):
		QThread.__init__(self)
		self.connection = connection
		self.command = command

	def __del__(self):
		self.wait()

	def run(self):
		try:
			self.connection.conn.send(self.command.encode("utf8"))
		except:
			pass

class init(QWidget):
	def __init__(self, connection):
		super().__init__()
		self.connection = connection
		self.connection.shellOpen = True
		self.connection.shell = self
		self.cwd = ""
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.connection.hostname + " - Shell")
		vBox = QVBoxLayout()

		self.logOutput = QTextEdit()
		self.logOutput.setReadOnly(True)

		self.log("Shell Window Enabled")

		vBox.addWidget(self.logOutput)

		self.commandEntry = QLineEdit()
		self.commandEntry.returnPressed.connect(self.enterCommand)
		vBox.addWidget(self.commandEntry)

		self.setLayout(vBox)
		self.resize(600, 500)
		self.show()

		self.startCommandListener()

	def closeEvent(self, event):
		self.connection.shellOpen = False
		self.connection.shell = None
		event.accept()

	def log(self, text):
		self.logOutput.setText(self.logOutput.toPlainText() + text + "\n")
		self.logOutput.moveCursor(QTextCursor.End)

	def enterCommand(self):
		command = self.commandEntry.text()
		self.commandEntry.setText("")
		self.log("Sent Command: " + command)
		self.sendCommand(command)

	def startCommandListener(self):
		self.scanThread = shellReciever(self.connection)
		self.scanThread.signal.connect(self.handleCommandOutput)
		self.scanThread.start()

	def handleCommandOutput(self, output):
		self.log(output)

	def sendCommand(self, command):
		commandSender = sendCommand(self.connection, "shell: " + command)
		commandSender.start()