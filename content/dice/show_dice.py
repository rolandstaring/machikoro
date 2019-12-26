
import sys
import random

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc


class App(qtw.QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'Roll the dice'
		self.left = 10
		self.top = 10
		self.width = 300
		self.height = 300
		self.counter = 0
		self.rnd_int1 = 0
		self.rnd_int2 = 0
		self.interval_seconds = 0.2
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		
		
		self.timer = qtc.QTimer()
		self.timer.setInterval(self.interval_seconds *1000)
		self.timer.timeout.connect(self.dobbel)
		
		# Create widget
		
		self.gridlayout = qtw.QGridLayout()
		self.setLayout(self.gridlayout)
		
		self.dobbelen_button = qtw.QPushButton(
			"Dobbel",
			clicked= self.show_next_pixmap)
		
		self.dice1 = qtw.QLabel(self)
		self.dice2 = qtw.QLabel(self)
		self.pm_list = []
		for n in range(1,7):
			file_name = 'dice_' + str(n) + '.jpg'
			self.pm_list.append(qtg.QPixmap(file_name))
		
		
		self.gridlayout.addWidget(self.dice1,1,1)
		self.gridlayout.addWidget(self.dice2,1,2)
		self.gridlayout.addWidget(self.dobbelen_button,2,1,2,1)
		self.dice1.setPixmap(self.pm_list[0])	
		self.dice2.setPixmap(self.pm_list[0])
		self.show()
		
	def dobbel(self):
		self.show_next_pixmap()	
	
		
	def the_end(self):
		self.timer.stop()
		self.dice1.setPixmap(self.pm_list[self.rnd_int1-1])	
		self.dice2.setPixmap(self.pm_list[self.rnd_int2-1])	
		self.counter = 0
		self.show()
		
	def show_next_pixmap(self):
		if self.counter == 10:
			self.the_end()
			return None
		self.dice1.clear()
		self.dice2.clear()
		self.rnd_int1 = random.randrange(1,7,1)
		self.rnd_int2 = random.randrange(1,7,1)
		
		self.dice1.setPixmap(self.pm_list[self.rnd_int1-1])
		self.dice2.setPixmap(self.pm_list[self.rnd_int2-1])
		
		self.counter+=1
		self.timer.start()	
		self.show()

		
		

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())