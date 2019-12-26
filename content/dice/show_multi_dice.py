
import sys
import random

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc


class Dice(qtw.QWidget):

	def __init__(self, nr_of_dices ):
		super().__init__()
		self.title = 'Roll the dice'
		self.left = 10
		self.top = 10
		self.width = 150
		self.height = 150
		self.rounds = 0
		
		self.finish = False
		
		self.nr_of_dices = nr_of_dices
		self.dice_list = []
		self._rnd_list = []
		
		self.interval_seconds = 0.2
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width*self.nr_of_dices, self.height)
	
		self.timer = qtc.QTimer()
		self.timer.setInterval(self.interval_seconds *1000)
		self.timer.timeout.connect(self.roll_dices)
		
		# Create widget
		
		self.gridlayout = qtw.QGridLayout()
		self.setLayout(self.gridlayout)
		
		#self.dobbelen_button = qtw.QPushButton(
		#	"Dobbel",
		#	clicked= self.show_next_pixmap)
		
		
		self.pm_list = []
		for n in range(1,7):
			file_name = 'dice/dice_' + str(n) + '.jpg'
			self.pm_list.append(qtg.QPixmap(file_name))
		
		
		for n in range(self.nr_of_dices):
			self.dice = qtw.QLabel(self)
			self.dice_list.append(self.dice)
		
		for dice in self.dice_list:
			self.gridlayout.addWidget(dice, 1,self.dice_list.index(dice)+1 )
			self.dice.setPixmap(self.pm_list[0])
			
		#self.gridlayout.addWidget(self.dobbelen_button,2,1,2,1)
		self.show()
		
	def run(self):
		self.roll_dices()	
		
	def stop(self):
		self.timer.stop()
		count = 0
		for dice in self.dice_list:
			dice.setPixmap(self.pm_list[self._rnd_list[count]-1])
			count +=1
	
		self.counter = 0
		self.show()
		qtc.QTimer.singleShot(2 *1000, self.close)
	
		
	def roll_dices(self):
		if self.rounds == 10:
			self.stop()
			return None
		self.randomize_all_dices()
		
		self.rounds+=1
		self.timer.start()	
		self.show()

	def randomize_all_dices(self):
		rnd_round_l = []
		for dice in self.dice_list:
			dice.clear()
			rnd_int = random.randrange(1,7,1)
			dice.setPixmap(self.pm_list[rnd_int-1])
			rnd_round_l.append(rnd_int)
		self._rnd_list = rnd_round_l


	def __getitem__(self,position):
		return self._rnd_list[position]	
		

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	dice = Dice(1)

	sys.exit(app.exec_())