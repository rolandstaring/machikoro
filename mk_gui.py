
import sys
import random
import sip
import mk_core as mk

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc
from PyQt5 import QtMultimedia as qtm


class Global():
	def __init__(self):
		self.buy_fase = False
		self.sounds = {
    		'click': qtm.QSound("content/geluid/click.wav"),
    		'card': qtm.QSound("content/geluid/card.wav"),
    		'dice': qtm.QSound("content/geluid/dice.wav"),
    		'cheer': qtm.QSound("content/geluid/cheer.wav"),
		}
		
	def set_buy_fase(self,bool):
		self.buy_fase = bool
		
class TightListWidget(qtw.QListWidget):
	def __init__(self):
		super().__init__()
		
	def set_size(self):
		self.width = 1.4 * self.sizeHintForColumn(0) + 3 * self.frameWidth()
		self.height = self.sizeHintForRow(0) * (1.2 *self.count()) + 3 * self.frameWidth()
		self.setFixedSize( self.width, self.height)
	
	def scroll_bottom(self,list):
		if len(list)>0:
			item = self.findItems(list[-1], qtc.Qt.MatchRegExp)[-1]
			self.scrollToItem(item)

class DiceLabel(qtw.QLabel):
	clicked = qtc.pyqtSignal()
	
	def __init__(self):
		super().__init__()
		
		#self.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
		#self.setLineWidth(3)
		
	def mousePressEvent(self,event):
		glob.sounds['dice'].play()
		self.clicked.emit() 

class Dice(qtw.QWidget):
	dice_ready = qtc.pyqtSignal(list)
	
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
		self.setGeometry(self.left, self.top, self.width*self.nr_of_dices, self.height*self.nr_of_dices)
	
		self.timer = qtc.QTimer()
		self.timer.setInterval(self.interval_seconds *1000)
		self.timer.timeout.connect(self.roll_dice)
		
		# Create widget
		
		self.gridlayout = qtw.QGridLayout()
		self.setLayout(self.gridlayout)
		
		
		self.pm_list = []
		for n in range(1,7):
			file_name = 'content/dice/dice_' + str(n) + '.jpg'
			self.pm_list.append(qtg.QPixmap(file_name))
		
		
		for n in range(self.nr_of_dices):
			self.dice = DiceLabel()
			self.dice_list.append(self.dice)
			self.dice.clicked.connect(self.run)
		
		for dice in self.dice_list:
			self.gridlayout.addWidget(dice, 1,self.dice_list.index(dice)+1 )
			self.dice.setPixmap(self.pm_list[0])
		
		self.show()
		
	def run(self):
		self.roll_dice()	
		
	def stop_dice(self):
		self.timer.stop()
		count = 0
		for dice in self.dice_list:
			dice.setPixmap(self.pm_list[self._rnd_list[count]-1])
			count +=1
		self.counter = 0
		self.rounds=0
		self.dice_ready.emit(self._rnd_list)
		self.show()
		
	def roll_dice(self):
		if self.rounds == 10:
			self.stop_dice()
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

class MyCardLabel(qtw.QLabel):
	clicked = qtc.pyqtSignal(str)

	
	def __init__(self,filename, amount=6):
		super().__init__()
		self.filename = filename
		self.name = filename.split('_')[1]
		self.amount = amount
		
	def mousePressEvent(self,event):
		glob.sounds['click'].play()
		if glob.buy_fase == True:
			self.clicked.emit(self.filename)	
			
	def mouseDoubleClickEvent(self, event):
		kaart_info = qtw.QMessageBox()
		file_loc = 'content/kaarten_groot/' + self.filename + '.jpg'
		pixmap = qtg.QPixmap(file_loc)
		kaart_info.setIconPixmap(pixmap)
		kaart_info.addButton(qtw.QMessageBox.Abort)
		response = kaart_info.exec()
		if response == qtw.QMessageBox.Abort: kaart_info.close()
		
class GameWidget(qtw.QWidget):
	def __init__(self, players):
		super().__init__(modal=True)
		self.players = players
		self.player_widgets = []
		self.left = 800
		self.top = 600
		self.width = 200
		self.height = 100
		self.title = 'Machikoro Game Central'
		self.activePlayer = 0
		self.ronde = 1
		
		#self.extra_beurt= False
		self.speler_net_geweest_door_radiostation = False
		self.speler_net_geweest_door_dubbelgooien = False
		self.extra_beurt = False
		
		self.spel = mk.Spel(self.players)
		
		self.speler = self.spel.spelers_l[self.activePlayer]
		self.bank = BankWidget(self.spel)
		self.bank.buy_card.connect(self.buy_cards)	
		
		self.initUI()
		
	def initUI(self):

		
		file_loc = 'content/kaarten/koop_niets.jpg'
		self.koopnietslabel = MyCardLabel('koop_niets')
		self.koopnietspixmap = qtg.QPixmap(file_loc)
		self.koopnietslabel.setPixmap(self.koopnietspixmap)
		self.koopnietslabel.clicked.connect(self.buy_nothing)
				
		self.hlayout = qtw.QHBoxLayout()
		self.setLayout(self.hlayout)
		
		self.tab_widget = qtw.QTabWidget()
	
		for player in self.players:
			player_widget = PlayerWidget(player, self.spel)
			player_widget.buy_goalcard.connect(self.buy_goalcards)
			tab_scrollarea = qtw.QScrollArea()
			self.tab_widget.addTab(tab_scrollarea, player)
			tab_scrollarea.setWidget(player_widget)
			tab_scrollarea.setWidgetResizable(True)
			player_widget.show()
			self.player_widgets.append(player_widget)
	
		self.vleftlayout = qtw.QVBoxLayout()
		self.vrightlayout = qtw.QVBoxLayout()
		
		self.hlayout.addLayout(self.vleftlayout)
		self.hlayout.addLayout(self.vrightlayout)
		
		
		bank_scrollarea = qtw.QScrollArea()
		bank_scrollarea.setWidget(self.bank)
		bank_scrollarea.setWidgetResizable(True)
		
		self.groupbox_messages = qtw.QGroupBox('Messages')
		self.vrightlayout.addWidget(self.groupbox_messages)
		self.vrightlayout.addWidget(bank_scrollarea)	
		
		self.messages_list_widget = TightListWidget()
		self.messages_layout = qtw.QHBoxLayout()
		self.groupbox_messages.setLayout(self.messages_layout)
		self.messages_layout.addWidget(self.messages_list_widget)
		self.messages_layout.addWidget(self.koopnietslabel)
		self.groupbox_messages.setMaximumSize(800,170)
		
		
		# topright layout with Stand and Dobbel groupbox
		self.groupbox_score = qtw.QGroupBox('Stand')
		self.groupbox_dobbel = qtw.QGroupBox('Dobbel')
		self.topleftlayout = qtw.QHBoxLayout()
		self.vleftlayout.addLayout(self.topleftlayout)
		self.topleftlayout.addWidget(self.groupbox_score)
		self.topleftlayout.addWidget(self.groupbox_dobbel)
		
		
		self.gridlayout_score = qtw.QGridLayout()
		self.dobbellayout = qtw.QVBoxLayout()
		
		self.groupbox_dobbel.setLayout(self.dobbellayout)
		self.groupbox_score.setLayout(self.gridlayout_score)

		self.dice_widget = Dice(1)
		self.dobbellayout.addWidget(self.dice_widget)
		self.dice_widget.dice_ready.connect(self.process_dice_result)
		
		
		self.vleftlayout.addWidget(self.tab_widget)
		
		self.muntlijst_l = []	
		
		for speler_nr in range(len(self.players)):
			
			self.gridlayout_score.addWidget(qtw.QLabel(self.players[speler_nr]), 3+speler_nr, 0)
			self.speler = self.spel.spelers_l[speler_nr]
			munten = self.speler.aantalMunten()
			munt_l = [str(munten)]
			self.muntlijst = TightListWidget()
			self.muntlijst.addItems(munt_l)
			self.gridlayout_score.addWidget(self.muntlijst, 3+speler_nr,1)
			self.muntlijst.set_size()
			self.muntlijst_l.append(self.muntlijst)

		self.groupbox_score.setMaximumSize(300,200)
		self.groupbox_dobbel.setMaximumSize(300,200)
		
		self.setWindowTitle(self.title)
		#self.setGeometry(self.left, self.top, self.width, self.height)
		message = self.players[self.activePlayer] + ' moet dobbelen'
		self.messages_list_widget.addItems([message])
		#self.refresh_ronde()
		self.refresh_cards()
		self.showMaximized()
		
	def extra_dobbelen(self,dobbel_resultaat):
		speler =  self.spel.spelers_l[self.activePlayer]
		xt_dobbel = qtw.QMessageBox()
		xt_dobbel.setText('Nog een keer dobbelen?')
		text = speler.toonNaam() + ' je hebt gegooid ' + str(dobbel_resultaat) + '\n' + ' Wil je nog een keer dobbelen?'
		xt_dobbel.setInformativeText(text)
		xt_dobbel.addButton(qtw.QMessageBox.Yes)
		xt_dobbel.addButton(qtw.QMessageBox.No)
		response = xt_dobbel.exec()
		if response == qtw.QMessageBox.Yes: return True
		if response == qtw.QMessageBox.No: return False 
	
	def vraag_om_aantal_dobbelstenen(self):
		speler =  self.spel.spelers_l[self.activePlayer]
		vraag_tekst = self.players[self.activePlayer] + ' met hoeveel dobbelstenen wil je werpen?'
		keuzes = ("1","2")
		antwoord, okPressed = qtw.QInputDialog.getItem(self, "Kies dobbelstenen ",vraag_tekst, keuzes, speler.get_dice_mem(), False)
		if okPressed and antwoord:
			speler.set_dice_mem(int(antwoord)-1)
			return int(antwoord)	
		
	def verwerk_dobbel_resultaat(self,dobbel_resultaat):
		speler = self.spel.spelers_l[self.activePlayer]
		messages_l = self.spel.verwerkRegels(speler,dobbel_resultaat) 
		return messages_l
	
	def refresh_all_cards(self):
		for player_widget in self.player_widgets:
			player_widget.get_inventory()
			player_widget.showCards()
			player_widget.show()
	
	def refresh_cards(self):
		active_player_widget = self.player_widgets[self.activePlayer]
		active_player_widget.activateWindow()
		active_player_widget.show()
		
		
		self.bank.refresh_cards()
		#self.bank.draw_cards()
		
		self.tab_widget.setCurrentIndex(self.activePlayer)
				
	def refresh_ronde(self):
		self.rondeList.clear() 
		self.rondeList.addItems([str(self.spel.toonRonde())])
	
	def number_of_dice(self):
		self.dobbellayout.removeWidget(self.dice_widget)
		self.dice_widget.deleteLater()
		self.dice_widget = None
		
		speler = self.spel.spelers_l[self.activePlayer]
		if speler.aantalDobbelstenen() == 2:
			db_wens = self.vraag_om_aantal_dobbelstenen()
			self.dice_widget = Dice(db_wens)
		else:
			self.dice_widget = Dice(1)
		
		
		self.dobbellayout.addWidget(self.dice_widget)
		self.dice_widget.dice_ready.connect(self.process_dice_result)
	
	def van_naam_naar_speler(self, speler_naam):
		speler_nr  = 0
		for naam in self.players:
			if speler_naam == naam:
				return self.spel.spelers_l[speler_nr]	
			speler_nr += 1
	
	def namen_lijst_zonder_beurtspeler(self):
		beurt_speler = self.players[self.activePlayer]
		
		namen_l = []
		for naam in self.players:
			if naam != beurt_speler:
				namen_l.append(naam)
		
		return namen_l
			
	def vraag_om_andere_speler(self, reden):
		keuzes = self.namen_lijst_zonder_beurtspeler()
		antwoord, okPressed = qtw.QInputDialog.getItem(self, "Kies speler", reden , keuzes, 0, False)
		if okPressed and antwoord:
			return self.van_naam_naar_speler(antwoord)
	
	def kies_andere_speler(self,reden):
		if len(self.namen_lijst_zonder_beurtspeler()) == 1:
			return self.van_naam_naar_speler(self.namen_lijst_zonder_beurtspeler()[0])
		else:
			return self.vraag_om_andere_speler(reden)
	
	def kies_kaart_voor_wissel(self, speler):
		keuzes = speler.namenSpelkaarten()
		if speler.toonNaam() == self.players[self.activePlayer]:
			naam_speler = ' jezelf'
		else:
			naam_speler = speler.toonNaam() 
		message = "Kies kaart van " + naam_speler
		
		antwoord, okPressed = qtw.QInputDialog.getItem(self, "Kies kaart", message, keuzes, 0, False)
		if okPressed and antwoord:
			return antwoord
			
	def wissel_de_kaarten(self,kaartnaam_van_gekozen_speler,kaartnaam_van_jezelf, gekozen_speler,speler):
		#### selecteer de gekozen kaart van de gekozen speler
		index_nr1 = gekozen_speler.namenSpelkaarten().index(kaartnaam_van_gekozen_speler)
		kaart_van_gekozen_speler = gekozen_speler.spelkaarten_l.pop(index_nr1)
		
		## selecteer de kaart van de speler met de beurt
		index_nr2 = speler.namenSpelkaarten().index(kaartnaam_van_jezelf)
		kaart_van_speler = speler.spelkaarten_l.pop(index_nr2)
		
		## voeg de kaarten toe aan de kaartsets van de spelers
		gekozen_speler.voegtoeKaart(kaart_van_speler)
		speler.voegtoeKaart(kaart_van_gekozen_speler)
		
		self.refresh_all_cards()
	
	def iemand_gewonnen(self):
		winnaar = self.players[self.activePlayer]
		gewonnen = qtw.QMessageBox()
		gewonnen.setText('Gefeliciteerd!')
		text = winnaar + ' heeft het spel gewonnen!! '
		gewonnen.setInformativeText(text)
		gewonnen.addButton(qtw.QMessageBox.Abort)
		response = gewonnen.exec()
		if response == qtw.QMessageBox.Abort: gewonnen.close()			
	
	def process_dice_result(self,dobbel_resultaat):
		
		#dobbel_resultaat = [6] ### testen 
		
		speler = self.spel.spelers_l[self.activePlayer]
		self.spel.dubbelgooienBeurt = False
		#### Check of er twee keer hetzelfde getal gegooid is. Als speler 'pretpark' heeft mag hij nog een keer
		if len(dobbel_resultaat) == 2 and dobbel_resultaat[0] == dobbel_resultaat[1] and speler.dubbelGooi() == True:
			self.spel.dubbelgooienBeurt = True
			self.extra_beurt = True
	
		## Als je 'radiostation' hebt mag je kiezen nog een keer te dobbelen.
		elif speler.doelkaartGehaaldSpeler('Radiostation') == True and self.speler_net_geweest == False:
			if self.extra_dobbelen(dobbel_resultaat)== True:
				self.speler_net_geweest = True			
				return							#opnieuw dobbelen
			else:
				self.dice_widget.setDisabled(True)
		
		else:			
			self.dice_widget.setDisabled(True)
		
		
		###### Toon dobbel resultaat 
		
		
		result_msg = self.players[self.activePlayer] + ' gooit ' + str(dobbel_resultaat)
		self.messages_list_widget.addItems([result_msg])

		###### Werk alle inkomsten bij op basis van dobbel resultaat
		
		messages_dobbelen = self.verwerk_dobbel_resultaat(sum(dobbel_resultaat))
		
		###### Verwerk de kaarten TV-STation en Bedrijvencomplex die een dialoog vereisen
		
		messages_gebouwen = []
		
		for speelkaart in  speler.toonSpelkaarten():
			if speelkaart.toonNaam() == 'TV-Station' and sum(dobbel_resultaat) == 6:
				gekozen_speler = self.kies_andere_speler('Kies speler voor 5 munten')
				t = mk.Transactie(gekozen_speler, speler, 5, ' TV-Station')
				t.verwerk()
				messages_gebouwen.append(t.beschrijf())
				
		for speelkaart in  speler.toonSpelkaarten():
			if speelkaart.toonNaam() == 'Bedrijvencomplex' and sum(dobbel_resultaat) == 6:
				gekozen_speler = self.kies_andere_speler('Kies speler waar je kaart van wil')
				kaartnaam_van_gekozen_speler = self.kies_kaart_voor_wissel(gekozen_speler) 
				kaartnaam_van_jezelf = self.kies_kaart_voor_wissel(speler)
				self.wissel_de_kaarten(kaartnaam_van_gekozen_speler,kaartnaam_van_jezelf,gekozen_speler, speler)
				message_wissel = speler.toonNaam() + ' ruilt ' + kaartnaam_van_jezelf + ' met ' +  kaartnaam_van_gekozen_speler + ' van ' + gekozen_speler.toonNaam()
				messages_gebouwen.append(message_wissel)
		
		
		###### Toon inkomsten op basis van dobbel resultaat aan spelers
		
		dlist = []
		if len(messages_dobbelen) > 0:
			str_list_msg_dobbelen = self.unnest_list(messages_dobbelen)
			for str_msg in str_list_msg_dobbelen:
				dlist.append(str_msg)
		
		fasechange_msg = self.players[self.activePlayer] + ' mag kaart kopen'
		dlist.append(fasechange_msg)
		
		
		#####  Update alle widgets
		self.messages_list_widget.addItems(messages_gebouwen) 
		self.messages_list_widget.addItems(dlist) 
		self.messages_list_widget.scroll_bottom(dlist)
	
		
		self.update_muntlijst()
		self.speler_net_geweest = False		
		glob.set_buy_fase(True)# na het dobbelen mag je kaarten kopen
		#self.update_ronde()
	
	
	def update_muntlijst(self):
		
		for speler_nr in range(len(self.players)):
			self.muntlijst_l[speler_nr].clear()
			
			self.speler = self.spel.spelers_l[speler_nr]
			munten = self.speler.aantalMunten()
			munt_l = [str(munten)]
			self.muntlijst_l[speler_nr].addItems(munt_l)
	
	def unnest_list(self,l):
		y =[]
		for i in l:
			for j in i:
				y.append(j)
		return y
	
	def extra_dobbelen(self,dobbel_resultaat):
		speler =  self.spel.spelers_l[self.activePlayer]
		xt_dobbel = qtw.QMessageBox()
		xt_dobbel.setText('Nog een keer dobbelen?')
		text = speler.toonNaam() + ' je hebt gegooid ' + str(dobbel_resultaat) + '\n' + ' Wil je nog een keer dobbelen?'
		xt_dobbel.setInformativeText(text)
		xt_dobbel.addButton(qtw.QMessageBox.Yes)
		xt_dobbel.addButton(qtw.QMessageBox.No)
		response = xt_dobbel.exec()
		if response == qtw.QMessageBox.Yes: return True
		if response == qtw.QMessageBox.No: return False 
					
	def switch_user(self):
		
		if self.spel.iemandGewonnen() == True:
			glob.sounds['cheer'].play()
			self.iemand_gewonnen()
			return	
		
		if self.extra_beurt != True:
			self.activePlayer += 1
	
		if self.activePlayer == len(self.players):
			self.activePlayer = 0
			self.spel.plusRonde()
		
		self.dice_widget.setDisabled(False)
		
		message = self.players[self.activePlayer] + ' moet dobbelen'
		self.messages_list_widget.addItems([message])
		self.messages_list_widget.scroll_bottom([message])
		
		self.extra_beurt = False
		self.refresh_cards()
		#self.refresh_ronde()
		self.number_of_dice()
	
	def buy_nothing(self):
		glob.set_buy_fase(False)
		qtc.QTimer.singleShot(1*1000,self.switch_user)
	
	def buy_goalcards(self,goalcard):
		active_player_widget = self.player_widgets[self.activePlayer]
		
		trans = self.spel.koopDoelkaart(self.activePlayer, goalcard.split('_')[1])
		self.messages_list_widget.addItems([trans])
		self.messages_list_widget.scroll_bottom([trans])
		
		
		if trans == 'Deze kaart kan je van je geld niet kopen' or trans == 'Deze kaart is niet meer beschikbaar bij de bank':
			pass
		else:
			active_player_widget.showGoalcards()
			self.update_muntlijst()
			glob.set_buy_fase(False)	
			glob.sounds['card'].play()		
			qtc.QTimer.singleShot(1*1000,self.switch_user)	
		
	def buy_cards(self, card):
		active_player_widget = self.player_widgets[self.activePlayer]
		
		trans = self.spel.koopSpelkaart(self.activePlayer, card.split('_')[1])
		self.messages_list_widget.addItems([trans])
		self.messages_list_widget.scroll_bottom([trans])
		
		
		if trans == 'Deze kaart kan je van je geld niet kopen' or trans == 'Deze kaart is niet meer beschikbaar bij de bank':
			pass
		else:
			active_player_widget.get_inventory()
			active_player_widget.showCards()
			self.update_muntlijst()
			glob.set_buy_fase(False)
			glob.sounds['card'].play()
			qtc.QTimer.singleShot(1*1000,self.switch_user)
	
class PlayerWidget(qtw.QWidget):
	buy_goalcard = qtc.pyqtSignal(str)

	def __init__(self, name, spel):
		super().__init__(modal=True)
		self.left = 800
		self.top = 10
		self.width = 600
		self.height = 600
		self.title = 'Cards of ' + name 
		self.dir = 'content/kaarten/'
		self.goals_vk = []
		self.goals_ak = []
		self.inventory = []
		self.name = name
		self.spel = spel
		self.speler_nr = self.spel.spelers_namen.index(self.name)
		self.speler = self.spel.spelers_l[self.speler_nr]
		
		
		
		self.cards = []
		self.get_filenames()
		self.get_inventory()
		self.initUI()
		
		self.showCards()
		self.showGoalcards()
	

		
	def get_filenames(self):
		self.goals_ak = [str(f + '_ak') for f in self.speler.filenamenDoelkaarten() ]
		self.goals_vk = [str(f + '_vk') for f in self.speler.filenamenSpelkaarten() ]
	
	def get_inventory(self):
		
		self.inventory	= [str(f) for f in self.speler.filenamenSpelkaarten() ]
		
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		vlayout = qtw.QVBoxLayout()
		self.setLayout(vlayout)
		
		self.groupbox_goals = qtw.QGroupBox('Goals')
		self.groupbox_cards = qtw.QGroupBox('Cards')	
			
		vlayout.addWidget(self.groupbox_goals)
		vlayout.addWidget(self.groupbox_cards)
		
		self.gridlayout_goals = qtw.QGridLayout()
		self.gridlayout_cards = qtw.QGridLayout()

		self.groupbox_goals.setLayout(self.gridlayout_goals)
		self.groupbox_cards.setLayout(self.gridlayout_cards)
		self.show()
	
	def showGoalcards(self):
		
		self.glb_list = []
		files_doelen = []
		
		for doelkaart in self.speler.doelkaarten_l:
			if doelkaart.doelkaartGehaald() == True:
				file = doelkaart.toonFilenaam() + '_vk'
				files_doelen.append(file)
			else:
				file = doelkaart.toonFilenaam() + '_ak'
				files_doelen.append(file)
		
		for filename in files_doelen:
			file_loc = self.dir + filename + '.jpg'
			label = MyCardLabel(filename)
			label.clicked.connect(self.whenClickedlabel)
			pixmap = qtg.QPixmap(file_loc)
			label.setPixmap(pixmap)
			self.glb_list.append(label)		
		
		for g_label in self.glb_list:
			self.gridlayout_goals.addWidget(g_label,1,self.glb_list.index(g_label)+1)
		
		
	def showCards(self):
		self.lb_list = []
				
		mycardset = set(self.inventory)
		uni_inventory = list(mycardset)
		sor_uni_inv = sorted(uni_inventory)
		
		self.lq_list = []
		
		for name in sor_uni_inv:
			file_loc = self.dir + name + '.jpg'
			label = MyCardLabel(name)
			listq = TightListWidget()	
			listq.addItems([str(self.inventory.count(name))])
			listq.set_size()
			pixmap = qtg.QPixmap(file_loc)
			label.setPixmap(pixmap)
			#label.clicked.connect(self.whenClickedLabel)
			self.lb_list.append(label)	
			self.lq_list.append(listq)
		
		r=2
		k=1
		for label in self.lb_list:
			self.gridlayout_cards.addWidget(label,r,k)
			self.gridlayout_cards.addWidget(self.lq_list[self.lb_list.index(label)],r+1,k)
			k+=1
			if (self.lb_list.index(label)+1)%4 == 0:
				r+=2
				k=1
		
		self.resize(pixmap.width(),pixmap.height())		
		self.show()
	
	def buyCards(self,card):
		self.inventory.append(card)
		self.cards.append(card.split('_')[1])
		self.showCards()		
	
	def whenClickedlabel(self,goalcard):
		self.buy_goalcard.emit(goalcard)

	
	def __getitem__(self,position):
		return	self.cards[position]
				
class BankWidget(qtw.QWidget):
	buy_card = qtc.pyqtSignal(str)
	
	def __init__(self,spel):
		super().__init__()
		self.title = 'The Bank owns the following cards'
		self.left = 10
		self.top = 10
		self.width = 600
		self.height = 600
		self.dir = 'content/kaarten/'
		self.files = []
		self.spel = spel
		
		self.initUI()
		
		self.get_cards()
		self.draw_cards()
		
	def get_cards(self):
		self.files = self.spel.bank.lijstfilenamenSpelkaarten()		
	
	def refresh_cards(self):
		self.get_cards()
		self.draw_cards()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.vlayout = qtw.QVBoxLayout()
		self.setLayout(self.vlayout)
		
		self.gridlayout = qtw.QGridLayout()
		#self.setLayout(self.gridlayout)
			
		self.groupbox_bank = qtw.QGroupBox('Bank')
		self.vlayout.addWidget(self.groupbox_bank)
		
		self.groupbox_bank.setLayout(self.gridlayout)
		
		
		# Create widget
	def draw_cards(self):	
		lb_list = []
		lq_list = []
		
		sorted_files = sorted(self.files)
		
		for filename in sorted_files:
			#set the count of the cards
			name = filename.split('_')[1]
			listq = TightListWidget()	
			listq.addItems([str(self.spel.bank.aantalSpelkaart(name))])
			listq.set_size()
			lq_list.append(listq)
			
			# set the display of the cards
			file_loc = self.dir + filename + '.jpg'
			label = MyCardLabel(filename)
			pixmap = qtg.QPixmap(file_loc)
			label.setPixmap(pixmap)
			label.clicked.connect(self.whenClickedLabel)
			lb_list.append(label)
			
			
		
		self.resize(pixmap.width(),pixmap.height())
		
		r=2
		k=1
		for label in lb_list:
			self.gridlayout.addWidget(label,r,k)
			self.gridlayout.addWidget(lq_list[lb_list.index(label)],r+1,k)
			k+=1
			if (lb_list.index(label)+1)%4 == 0:
				r+=2
				k=1
		
			
		#for label in self.lb_list:
		#	label.mousePressEvent()
		
		self.show()
	
	def whenClickedLabel(self,card):
		self.buy_card.emit(card)
		
class MainWindow(qtw.QMainWindow): # change to mainwindow
	def __init__(self):
	
		super().__init__()
		# Main UI code goes here
		
		self.players = []
		
		self.cwidget = qtw.QWidget()	
		self.vlayout = qtw.QVBoxLayout()
		self.cwidget.setLayout(self.vlayout)
		
		self.players_label = qtw.QLabel('Spelers')
		self.addplayer_button = qtw.QPushButton(
			"Add player",
			clicked= self.add_player)
			
		self.start_button = qtw.QPushButton(
			"Start Game",
			clicked= self.start_game)
		
		self.player_list = qtw.QListWidget()
		self.player_list.addItems(self.players)
		
		self.vlayout.addWidget(self.player_list)
		self.vlayout.addWidget(self.addplayer_button)
		self.vlayout.addWidget(self.start_button)
		
		
		
		self.setCentralWidget(self.cwidget)
		
		self.show()
		
		#################
		# The Statusbar #
		#################
		
		self.statusBar().showMessage('Welcome to MachiKoro')
		

		###############j
		# The menubar #
		###############
		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)

		# add submenus to a menu
		file_menu = menubar.addMenu('File')
		game_menu = menubar.addMenu('Game')
		help_menu = menubar.addMenu('Help')
		exit_menu = menubar.addMenu('Exit')

		# add actions
		#new_player_action = game_menu.addAction('New Player',self.add_new_player)
		#new_game_action = game_menu.addAction('New Game',self.start_game)					
		#connect_action = game_menu.addAction('Open Connection', self.open_connection) 
		
		open_action = file_menu.addAction('Open')
		save_action = file_menu.addAction('Save')
		
		
		# add separator
		file_menu.addSeparator()

	def refresh_players(self):
		self.player_list.clear()
		self.player_list.addItems(self.players)
		
	def add_player(self):
		text, ok = qtw.QInputDialog.getText(self, 'Name of player', 'Enter your name:')
		if ok:
			self.players.append(text)
			self.refresh_players()
			
	
	def start_game(self):
		self.game_started = False
		self.cwidget = GameWidget(self.players) 
		self.setCentralWidget(self.cwidget)
		self.showMaximized()

##############################################
	

		
if __name__ == '__main__':
	
	app = qtw.QApplication(sys.argv)
	glob = Global()
	mw = MainWindow()
			
	sys.exit(app.exec_())