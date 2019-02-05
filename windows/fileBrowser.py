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
import stylesheets
import master

class queryFileData(QThread):

	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self, mainLayout):
		QThread.__init__(self)
		self.mainLayout = mainLayout

	def __del__(self):
		self.exec_()

	def run(self):
		self.signal.emit([self.getFiles(), self.getDirs()])
		#self.terminate()

	def getFiles(self):
		print("Querying For Files")
		self.mainLayout.connection.conn.send("getFiles".encode("utf8"))
		string = self.mainLayout.connection.conn.recv(1024 * master.chunkSize).decode()
		print("Recieved Files")
		files = string.split(",")
		return files

	def getDirs(self):
		print("Querying For Directories")
		self.mainLayout.connection.conn.send("getDirs".encode("utf8"))
		string = self.mainLayout.connection.conn.recv(1024 * master.chunkSize).decode()
		print("Recieved Directories")
		files = string.split(",")
		return files

class init(QWidget):
	def __init__(self, connection):
		super().__init__()
		self.connection = connection

		self.connection.fileBrowser = self

		self.cwd = self.getCwd()

		self.files = []
		self.dirs = []

		self.initUI()

	def initUI(self):
		
		#self.renderDirectory()
		self.refreshFileData()
		
		self.resize(600, 800)
		self.show()

	def handleDirData(self, data):
		self.renderDirectory(data[0], data[1])

	def renderDirectory(self, files, dirs):
		print("Rendering Directory")
		self.files = files
		self.dirs = dirs

		folderFont = QFont("Times", 8, QFont.Bold)
		fileFont = QFont("Times", 8) 

		textHolder = QVBoxLayout()

		for folder in self.dirs:
			fileLabel = QPushButton(folder)
			fileLabel.setFont(folderFont)
			fileLabel.setStyleSheet(stylesheets.folderButton)

			fileLabel.clicked.connect(partial(self.changeDir, folder))

			textHolder.addWidget(fileLabel)

		for file in self.files:
			fileLabel = QPushButton(file)
			fileLabel.setFont(fileFont)
			fileLabel.setStyleSheet(stylesheets.fileButton)

			fileLabel.clicked.connect(partial(self.readFile, file))

			textHolder.addWidget(fileLabel)

		textHolder.addStretch(1)

		self.deleteLayout(self.layout())
		self.setLayout(textHolder)

		self.cwd = self.getCwd()
		self.setWindowTitle(self.cwd + " - " + self.connection.hostname)

	def closeEvent(self, event):
		self.connection.fileBrowser = None
		event.accept()

	def getCwd(self):
		self.connection.conn.send("getCwd".encode("utf8"))
		return self.connection.conn.recv(1024 * master.chunkSize).decode()

	def refreshFileData(self):
		self.scanThread = queryFileData(self)
		self.scanThread.signal.connect(self.handleDirData)
		self.scanThread.start()

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

	def changeDir(self, directory):
		self.connection.conn.send(("cd: " + directory).encode("utf8"))
		self.cwd = self.getCwd()
		self.setWindowTitle(self.cwd + " - " + self.connection.hostname)
		#time.sleep(0.5)
		self.refreshFileData()

	def readFile(self, file):
		print("Reading File: " + file)
