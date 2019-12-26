import random

		
class Spel:
	def __init__(self, namen_lijst):
		
		self.spelers_namen =  namen_lijst	
		self.spelers_l = [] 
		self.maakSpelers()	
		self.dubbelgooienBeurt = False
		self.ronde = 1
		self.bank = Bank(len(self.spelers_namen))
		self.deelStartkaartenSpelers()
		self.winnaar = 'niemand'
		self.transactions = []
			
	def winnaarSpel(self):
		return self.winnaar
		
	def dubbelgooiBeurt(self):
		return self.dubbelgooienBeurt
	
	def aantalBeurten(self, speler_nr):
		return self.spelers_l[speler_nr].aantalBeurten() 
			
	def plusRonde(self):
		self.ronde += 1
		
	def toonRonde(self):
		return self.ronde
		
	def maakSpelers(self):	
		for s in range(len(self.spelers_namen)):
			# eerste speler = startspeler  krijgt 2 munten overige krijgen er 3
			if s == 0:
				self.spelers_l.append(Speler(self.spelers_namen[s],[],[],2))
			else:
				self.spelers_l.append(Speler(self.spelers_namen[s],[],[]))
	
	def deelStartkaartenSpelers(self):
		for speler_nr in range(len(self.spelers_namen)):
			self.deelStartkaartenSpeler(self.bank,speler_nr)
	
	def beurt(self):
		self.beurtSpeler(0)
	
	def kaartnameninBudget(self, speler_nr):
		spelkaarteninbudget_l =	 self.bank.spelkaarteninbudgetSpeler(self.spelers_l[speler_nr])
		doelkaarteninbudget_l =	 self.bank.doelkaarteninbudgetSpeler(self.spelers_l[speler_nr]) 
		
		spelkaart_namen = []
		for spelkaart in spelkaarteninbudget_l:
			spelkaart_namen.append(spelkaart.toonNaam())
		
		doelkaart_namen = []
		for doelkaart in doelkaarteninbudget_l:
			doelkaart_namen.append(doelkaart.toonNaam())
			
		return spelkaart_namen + doelkaart_namen
	

	def deelStartkaartenSpeler(self,bank,speler_nr):
		doelkaarten = bank.geefDoelkaarten()	
		self.spelers_l[speler_nr].voegtoeDoelkaarten(doelkaarten)
		
		spelkaarten = bank.geefStartkaarten()	
		self.spelers_l[speler_nr].voegtoeSpelkaarten(spelkaarten)
	
	
	def actieSpeler(self,speler_nr, kaart_naam):
		if len(kaart_naam) == 2:
			kaart_naam = self.bank.vankortnaarlangeNamen(kaart_naam)
		if self.bank.isSpelkaart(kaart_naam):
			self.koopSpelkaart(speler_nr, kaart_naam)
		elif self.bank.isDoelkaart(kaart_naam):
			self.koopDoelkaart(speler_nr,kaart_naam)
		else:
			#print 'Deze kaart ken ik niet'
			pass	
	
	def verwerkRegels(self,beurt_speler, dobbel_resultaat):
		alle_transacties_l = []
		for speler in self.spelers_l:
			regels = Regels(self.bank, speler, beurt_speler, dobbel_resultaat) # we maken de regels
			regels.verwerk_regelsSpelkaarten() # we passen ze toe
			#print(str(dobbel_resultaat))
			#print('regels voor ' + speler.toonNaam() + ' ' + str(regels.toonTransacties()))
			alle_transacties_l.append(regels.toonTransacties())
		
		return alle_transacties_l
			
	def printSpelkaarten(self, spelkaarten_l):
		for spelkaart in spelkaarten_l:
			spelkaart.printSpelkaart()
	
	def lijstSpelkaarten(self, spelkaarten_l):
		spelkaartennamen_l = []
		for spelkaart in spelkaarten_l:
			spelkaartennamen_l.append(spelkaart.toonNaam())
		return spelkaartennamen_l
	
	def printDoelkaarten(self, doelkaarten_l):
		for doelkaart in doelkaarten_l:
			doelkaart.printDoelkaart()
				
	def iemandGewonnen(self):
		# heeft een van de spelers alle doelkaarten gehaald?
		winnaar = False
		for speler_nr in range(len(self.spelers_namen)):
			if self.spelers_l[speler_nr].doelkaartenGehaaldSpeler() == True:
				winnaar = True					
				self.winnaar = self.spelers_l[speler_nr].toonNaam() 
				return True
		if winnaar == False:
			#print 'Niemand heeft nog gewonnen'						# nog geen winnaar
			return False
				
	def doelkaartenGehaaldSpeler(self,speler_nr):
		# check of een speler al zijn doelkaarten heeft gehaald
		self.spelers_l[speler_nr].doelkaartenGehaaldSpeler()
	
	def aantaldoelkaartenGehaaldSpeler(self,speler_nr):
		return self.spelers_l[speler_nr].aantaldoelkaartenGehaaldSpeler()
	
	def allespelersMunten(self, aantal_munten):
		for speler_nr in range(len(self.spelers_l)):
			self.spelers_l[speler_nr].plusMunten(aantal_munten) 
	
	def namenSpelers(self):
		return self.spelers_namen
	
	
	def koopSpelkaart(self, speler_nr, spelkaart_naam):
		## als kaart beschikbaar en budget beschikbaar
		speler = self.spelers_l[speler_nr]
			
		if	self.bank.kaartBeschikbaar(spelkaart_naam) == True:
			if	speler.aantalMunten() >= self.bank.watkostdieKaart(spelkaart_naam):	
				t = Transactie(speler, self.bank, self.bank.watkostdieKaart(spelkaart_naam), spelkaart_naam)
				t.verwerk()
		
				spelkaartvanbank = self.bank.verkoopSpelkaart(spelkaart_naam)				# krijg de kaart van de bank	
				self.spelers_l[speler_nr].voegtoeKaart(spelkaartvanbank)
				return t.beschrijf()						# voeg hem toe aan de speler
			else:
				return 'Deze kaart kan je van je geld niet kopen'
		else:
			return 'Deze kaart is niet meer beschikbaar bij de bank'
		
	def isDoelkaart(self, doelkaart_naam):
		if doelkaart_naam in self.bank.doelkaart_namen:
			return True
		else:
			return False	
		
	def koopDoelkaart(self,speler_nr, doelkaart_naam):
		speler = self.spelers_l[speler_nr]
		
		return_text = 'Er ging iets mis bij het kopen van een doelkaart'
		
		if speler.aantalMunten() >= speler.prijsDoelkaartSpeler(doelkaart_naam):
			t = Transactie(speler,self.bank, speler.prijsDoelkaartSpeler(doelkaart_naam), doelkaart_naam)	# geef geld voor doelkaart
			t.verwerk()
			
			speler.koopDoelkaart(doelkaart_naam) #  draag doelkaart over
			return_text = t.beschrijf()
			
		else:	
			return_text = 'Deze kaart kan je van je geld niet kopen'
			pass
		return return_text
		
	def __repr__(self):
		for s in range(len(self.spelers_l)):
			print('%s \n' % self.spelers_l[s])
		return 'End of list'	

class Transactie:
	def __init__(self, bron , doel, bedrag, reden):
		self.bron = bron	# speler of bank
		self.doel = doel	# speler of bank
		self.bedrag = bedrag	#int
		self.reden = reden	# string
		self.verwerkt = False  
		self.status = '' 
					
	def beschrijf(self):
		transaction_message =  self.bron.toonNaam() + ' betaald aan ' + self.doel.toonNaam() +	 ' ' + str(self.bedrag) + ' voor ' + self.reden
		return transaction_message
		
	def toonStatus(self):
		return self.status
	
	def transactieVerwerkt(self):
		return self.verwerkt
		
	def verwerk(self):
		if self.bron.aantalMunten() >= self.bedrag:
			self.bron.minMunten(self.bedrag) # bron/source geeft 
			self.doel.plusMunten(self.bedrag) # bestemming/destination ontvangt
			self.status = 'betaald'
		elif self.bron.aantalMunten() == 0:
			self.status = 'niet betaald'	# bron heeft geen geld	
		elif self.bron.aantalMunten() < self.bedrag and self.bron.aantalMunten() > 0:
			rest_munten = self.bron.aantalMunten()
			self.bron.minMunten(rest_munten) # bron geeft wat hij heeft 
			self.doel.plusMunten(rest_munten) # bestemming ontvangt wat bron heeft 
			self.status = 'deel betaald'		 # 
		self.verwerkt = True
		
class Regels:
	def __init__(self, bank, speler, beurt_speler, dobbel_resultaat): # pak het dobbel_resultaat en activeer transacties
		self.verwerkt = False
		self.beurt_speler = beurt_speler
		self.speler = speler
		self.bank = bank
		self.trigger_kaarten_l = [] # kaarten die getriggered worden door dobbel resultaat
		self.transacties_l = [] # alle transacties voor deze speler
		self.dobbel_resultaat = dobbel_resultaat
			
		self.selecteer_triggerSpelkaarten()
	
	def toonTransacties(self):
		return self.transacties_l
	
	def regelsVerwerkt(self):
		return self.verwerkt
	
	def selecteer_triggerSpelkaarten(self):
		# selecteer de kaarten die een hit hebben op basis van dobbel-resultaat
		for spelkaart in self.speler.toonSpelkaarten():
			for nr in spelkaart.toonNrlijst():
				#print(str(self.dobbel_resultaat))
				if self.dobbel_resultaat == nr:
					self.trigger_kaarten_l.append(spelkaart)
	
	
	def transactie(self, bron, doel, bedrag, reden):
		t = Transactie( bron, doel, bedrag, reden)
		t.verwerk()
		self.transacties_l.append(t.beschrijf())
		
	def bonus_koffie_brood(self):
		bonus = 0
		if self.speler.toonBonus() == True:
			bonus = 1
		return bonus
				
	def verwerk_regelsSpelkaarten(self):
		# alle spelers ontvangen inkomsten voor goederen
		#print(self.speler.toonNaam() + str(self.trigger_kaarten_l))
		self.verwerk_goederenSpelkaarten()
		self.verwerk_horecaSpelkaarten()
		self.verwerk_commercieleSpelkaarten()
		self.verwerk_gebouwenSpelkaarten()
		
		self.verwerkt = True
	
		
	### De Regels van de kaarten
	
	def verwerk_goederenSpelkaarten(self):
		for spelkaart in self.trigger_kaarten_l:
			if spelkaart.toonCategorie() == 'goederen':
				self.transactie(self.bank, self.speler, spelkaart.toonWaarde(), spelkaart.toonNaam())
				
		
	def verwerk_horecaSpelkaarten(self):
		for spelkaart in self.trigger_kaarten_l:
			if spelkaart.toonCategorie() == 'horeca':
				if self.speler != self.beurt_speler:  # je krijgt alleen wat als je het zelf niet gegooid hebt
					self.transactie(self.beurt_speler, self.speler, spelkaart.toonWaarde()+self.bonus_koffie_brood(), spelkaart.toonNaam()) 
	
	def verwerk_commercieleSpelkaarten(self):
		for spelkaart in self.trigger_kaarten_l:
			if spelkaart.toonCategorie() == 'commercieel':
				soort_l = spelkaart.toonSoort().split(' ')
				if self.speler == self.beurt_speler:
					if spelkaart.toonSoort() == 'brood':
						self.transactie(self.bank, self.speler, spelkaart.toonWaarde()+self.bonus_koffie_brood(), spelkaart.toonNaam())
					elif len(soort_l) == 2: # kaart is een fabriek
						bedrag = self.speler.aantalgoederenSpelkaarten(soort_l[0]) * spelkaart.toonWaarde()
						self.transactie(self.bank, self.speler, bedrag, spelkaart.toonNaam())
						
			 

	def verwerk_gebouwenSpelkaarten(self):
		spelkaarten_beurt_speler = self.beurt_speler.namenSpelkaarten()
		if self.speler != self.beurt_speler and  'Stadion' in spelkaarten_beurt_speler and self.dobbel_resultaat == 6:
			self.transactie(self.speler, self.beurt_speler, 2 , 'Stadion')

class Speler:
	def __init__(self, naam,  doelkaarten_l, spelkaarten_l , munten = 3, aantal_dobbelstenen = 1, aantal_beurten = 1):
		self.naam = naam
		self.bonus	= 0
		self.munten = munten
		self.doelkaarten_l = doelkaarten_l
		self.spelkaarten_l = spelkaarten_l
		self.aantal_dobbelstenen = aantal_dobbelstenen
		self.aantal_beurten = aantal_beurten
		self.dubbel_gooi  = False
		self.winkelcentrum_bonus = False
		self.dice_mem = 0
	
	def set_dice_mem(self, dice_nr):
		self.dice_mem = dice_nr
		
	def get_dice_mem(self):
		return self.dice_mem
	
	def bonusPlus(self,bonus):
		self.bonus += bonus

	def bonusMin(self,bonus):
		self.bonus -= bonus			
			
	def aantalBeurten(self):
		return self.aantal_beurten
		
	def vermogenKaarten(self):
		vermogen = 0
		for spelkaart in self.spelkaarten_l:
			vermogen += spelkaart.toonPrijs()
			
		for doelkaart in self.doelkaarten_l:
			if doelkaart.doelkaartGehaald() == True:
				vermogen += doelkaart.toonPrijs()	
		
		return vermogen		
		
	def aantalKaarten(self):
		return len(self.spelkaarten_l)
		
	def aantalDobbelstenen(self):
		return self.aantal_dobbelstenen
	
	def dubbelGooi(self):
		return self.dubbel_gooi
	
				
								
	def aantalgoederenSpelkaarten(self, soort): 
		teller = 0
		for spelkaart in self.spelkaarten_l:
			if spelkaart.toonSoort() == soort:
				teller += 1
		
		return teller				
					
	def voegtoeDoelkaarten(self, doelkaarten):
		for i in range(len(doelkaarten)):
			self.doelkaarten_l.append(doelkaarten[i])

	def voegtoeSpelkaarten(self, spelkaarten):
		for i in range(len(spelkaarten)):
			self.spelkaarten_l.append(spelkaarten[i])
			
	def voegtoeKaart(self, spelkaart):
		self.spelkaarten_l.append(spelkaart)
	
	def popKaart(self, spelkaart_naam):
		teller = 0
		for spelkaart in self.spelkaarten_l:
			if spelkaart.toonNaam() == spelkaart_naam:
				return self.spelkaarten_l.pop(teller)
			teller += 1
	
	
	def prijsDoelkaartSpeler(self, doelkaart_naam):
		for doelkaart in self.doelkaarten_l:
			if doelkaart.toonNaam() == doelkaart_naam:
				return doelkaart.toonPrijs()
	
	def koopDoelkaart(self,doelkaart_naam):
		for doelkaart in self.doelkaarten_l:
			if doelkaart.toonNaam() == doelkaart_naam:
				doelkaart.koopDoelkaart()
				self.effectDoelkaart(doelkaart_naam)
			 
	def effectDoelkaart(self, doelkaart_naam):
		#Treinstation, Winkelcentrum, Radiostation, Pretpark
		if doelkaart_naam == 'Treinstation':
				#'Je mag met twee dobbelstenen gooien'
				self.aantal_dobbelstenen = 2
		elif doelkaart_naam == 'Winkelcentrum':
				# 'Verhoog het aantal munten met 1 voor ?'
				self.winkelcentrum_bonus = True
		elif doelkaart_naam == 'Radiostation':
				#'Gooi je dobbelsteen nog een keer'
				self.aantal_beurten = 2 
		elif doelkaart_naam == 'Pretpark':
				#'Als je dubbel gooit ben je nog een keer'		
				self.dubbel_gooi = True
	
	
	def toonBonus(self):
		return self.winkelcentrum_bonus		
	
	def plusBeurten(self):
		self.aantal_beurten += 1
		
	def gooiDobbelstenen(self,aantal_dobbelstenen_wens):
		if self.aantal_dobbelstenen ==1 and aantal_dobbelstenen_wens ==1:
			#print self.aantal_dobbelstenen 
			return [random.randrange(1,7,1)]
		if self.aantal_dobbelstenen	 == 2 and aantal_dobbelstenen_wens ==1:
			#print self.aantal_dobbelstenen
			return [random.randrange(1,7,1)]
		elif self.aantal_dobbelstenen  == 2 and aantal_dobbelstenen_wens ==2:
			#print self.aantal_dobbelstenen
			return [random.randrange(1,7,1),random.randrange(1,7,1)]
				
	def inkomstenSpelkaarten(self, dobbel_resultaat):
		# bereken de punten op basis van spelkaarten
		munten = 0
		for spelkaart in self.spelkaarten_l:
			for nr in spelkaart.toonNrlijst():
				if dobbel_resultaat == nr:
					print('inkomsten voor' , spelkaart.toonNaam(),'=',	spelkaart.toonWaarde())
					munten += spelkaart.toonWaarde() 
		return munten
	
	def doelkaartenGehaaldSpeler(self): 
		gehaald = True
		for doelkaart in self.doelkaarten_l:
			if doelkaart.doelkaartGehaald() == False:
				gehaald = False
		return gehaald 
		
	def aantaldoelkaartenGehaaldSpeler(self):
		aantal = 0
		for doelkaart in self.doelkaarten_l:
			if doelkaart.doelkaartGehaald() == True:
				aantal += 1
		return aantal
		
		
	def doelkaartGehaaldSpeler(self, doelkaart_naam):
		for doelkaart in self.doelkaarten_l:
			if doelkaart.toonNaam() == doelkaart_naam and doelkaart.doelkaartGehaald()== True:
				return True
		return False
		
				
	def plusMunten(self, munten):
		self.munten +=	munten
		#self.rewards_l.append(munten)
			
	def minMunten(self,munten):
		if (self.munten - munten) >= 0:
			self.munten -= munten
			#self.rewards_l.append(-munten)
		else:
			self.munten = 0
			#self.rewards_l.append(0)
		
	def aantalMunten(self):
		return self.munten
	
	def toonNaam(self):
		return self.naam
	
	def vannaamnaarSpelkaartCategorie(self,naamSpelkaart):
		for spelkaart in self.spelkaarten_l:
			if spelkaart.toonNaam() == naamSpelkaart:
				return spelkaart.toonCategorie()
		return None
		
	
	def namenSpelkaarten(self):
		namenSpelkaarten = []
		for spelkaart in self.spelkaarten_l:
			namenSpelkaarten.append(spelkaart.toonNaam())
		return namenSpelkaarten
	
	def filenamenSpelkaarten(self):
		filenamenSpelkaarten = []
		for spelkaart in self.spelkaarten_l:
			filenamenSpelkaarten.append(spelkaart.toonFilenaam())
		return filenamenSpelkaarten
	
	def filenamenDoelkaarten(self):
		filenamenDoelkaarten = []
		for doelkaart in self.doelkaarten_l:
			filenamenDoelkaarten.append(doelkaart.toonFilenaam())
		return filenamenDoelkaarten
	
	
	def telSpelkaarten(self):
		kaarten = self.namenSpelkaarten()
		result = []
		double = []
		for k in kaarten:
			if k not in double:
				aantal = kaarten.count(k)
				count_str = k + ' ' + str(aantal)
				double.append(k)
				result.append(count_str)
			else:
				pass
		return result
	
	def namenDoelkaarten(self):
		namenDoelkaarten = []
		for doelkaart in self.doelkaarten_l:
			namenDoelkaarten.append(doelkaart.toonNaam())
		return namenDoelkaarten
	
	def naamenboolDoelkaarten(self):
		nenbDoelkaarten = []
		for doelkaart in self.doelkaarten_l:
			naamenboolstring = doelkaart.toonNaam() + ' ' + str(doelkaart.doelkaartGehaald())
			nenbDoelkaarten.append(naamenboolstring)
		return nenbDoelkaarten
	
	def printDoelkaarten(self):
		for doelkaart in self.doelkaarten_l:
			doelkaart.printDoelkaart()
			
	def printSpelkaarten(self):
		for spelkaart in self.spelkaarten_l:
			spelkaart.printSpelkaart()
		
	def toonSpelkaarten(self):
		return self.spelkaarten_l
	
	def toonDoelkaarten(self):
		return self.doelkaarten_l
		
	def __repr__(self):
		return '%s	munten = %s \n doel = %s \n stad = %s ' % (self.naam, self.munten, self.doelkaarten_l, self.spelkaarten_l)

class Bank:

	def __init__(self,aantal_spelers):
		self.munten = 100
		self.naam = 'bank'
		self.GGebouw_aantal = 4
		self.CGebouw_aantal = 6
		self.Goederen_aantal = 6
		self.Horeca_aantal = 6
		self.aantal_spelers = aantal_spelers
		
		
		#self.bedrijvencomplex_l = []
		self.stadion_l = []
		self.tvstation_l = []
		self.cafe_l = []
		self.restaurant_l = []
		self.graanveld_l = []
		self.veehouderij_l = []
		self.bos_l = []
		self.mijn_l = []
		self.appelboomgaard_l= []
		self.bakkerij_l = []
		self.supermarkt_l = []
		self.kaasfabriek_l = []
		self.meubelfabriek_l = []
		self.fruitgroentemarkt_l = []
		self.bedrijvencomplex_l = []
		
		self.treinstation_l = []
		self.winkelcentrum_l = []
		self.pretpark_l = []
		self.radiostation_l = []
		
		
		self.doelkaart_namen = ['Treinstation', 'Winkelcentrum','Pretpark','Radiostation']
		self.doelkaart_namen_kort = ['tr','wi','pr','ra']
		self.doelkaart_lijst = [Doelkaart('Treinstation',4,'Je mag met twee dobbelstenen gooien','4_Treinstation'),Doelkaart('Winkelcentrum',10, 'Verhoog het aantal munten met 1 voor koffie en brood','10_Winkelcentrum'),Doelkaart('Pretpark',16,'Als je dubbel gooit ben je nog een keer','16_Pretpark'),Doelkaart('Radiostation', 22,'Gooi je dobbelsteen nog een keer','22_Radiostation')]

		self.spelkaart_namen = ['Bedrijvencomplex','Stadion','TV-Station','Cafe','Restaurant','Graanveld','Veehouderij','Bos','Mijn','Appelboomgaard','Bakkerij','Supermarkt','Kaasfabriek','Meubelfabriek','FruitGroenteMarkt']
		self.spelkaart_namen_kort = ['be','st','tv','ca','re','gr','ve','bo','mi','ap','ba','su','ka','me','fr']
		self.spelkaart_lijsten = [self.bedrijvencomplex_l,self.stadion_l,self.tvstation_l, self.cafe_l, self.restaurant_l, self.graanveld_l , self.veehouderij_l , self.bos_l , self.mijn_l,self.appelboomgaard_l, self.bakkerij_l, self.supermarkt_l, self.kaasfabriek_l, self.meubelfabriek_l, self.fruitgroentemarkt_l]	
		self.voorraad_sk = {}
		self.voorraad_dk = {}
		self.korte_namen_sk = {}
		self.korte_namen_dk = {}
			
		self.maakKaarten()
	
	def maakKaarten(self): 
		# maak de voorraad van kaarten aan

		for i in range(self.Goederen_aantal):
			self.graanveld_l.append(Spelkaart('Graanveld',1, 'Ontvang 1 munt van de bank ongeacht wiens beurt',	'1_Graanveld', [1], 1, 'akkerbouw','goederen'))
			self.veehouderij_l.append(Spelkaart('Veehouderij',1,'Ontvang 1 munt van de bank ongeacht wiens beurt','2_Veehouderij',[2],1, 'veeteelt','goederen'))
			self.bos_l.append(Spelkaart('Bos',3,'Ontvang 1 munt van de bank ongeacht wiens beurt het is','5_Bos',[5],1,'grondstof','goederen'))
			self.mijn_l.append(Spelkaart('Mijn',6,'Ontvang 5 munten van de bank ongeacht wiens beurt het is','9_Mijn',[9],5,'grondstof','goederen'))
			self.appelboomgaard_l.append(Spelkaart('Appelboomgaard',3,'Ontvang 3 munten van de bank ongeacht wiens beurt het is','X10_Appelboomgaard',[10],3,'akkerbouw','goederen'))
		
		for i in range(self.CGebouw_aantal):
			self.bakkerij_l.append(Spelkaart('Bakkerij',1, 'Ontvang 1 munt van de bank als het jouw beurt is','2_Bakkerij',	[2,3],1, 'brood', 'commercieel'))
			self.supermarkt_l.append(Spelkaart('Supermarkt',2,'Ontvang 3 munten van de bank als het jouw beurt is','4_Supermarkt',[4],3,'brood','commercieel'))
			self.kaasfabriek_l.append(Spelkaart('Kaasfabriek',5,'Ontvang 3 munten van de bank voor elke veeteelt kaart die je bezit als het jouw beurt is','7_Kaasfabriek',[7],3,'veeteelt fabriek','commercieel'))
			self.meubelfabriek_l.append(Spelkaart('Meubelfabriek',3,'Ontvang 3 munten van de bank voor elke grondstof kaart die je bezig als het jouw beurt is','8_Meubelfabriek',[8],3,'grondstof fabriek','commercieel'))
			self.fruitgroentemarkt_l.append(Spelkaart('FruitGroenteMarkt',2,'Ontvang 3 munten van de bank voor elke akkerbouw kaart die je bezit als het jouw beurt is','X11_FruitGroenteMarkt',[11,12],3,'akkerbouw fabriek','commercieel'))	
			
		for i in range(self.GGebouw_aantal):
			self.bedrijvencomplex_l.append(Spelkaart('Bedrijvencomplex',8,'Je mag 1 kaart met een speler naar keuze ruilen als het jouw beurt is','6_Bedrijvencomplex',[6],8,'ruil','gebouw'))
			self.stadion_l.append(Spelkaart('Stadion',6,'Ontvang 2 munten van iedere speler als het jouw beurt is','6_Stadion',[6],2,'ieder','gebouw'))
			self.tvstation_l.append(Spelkaart('TV-Station',7,'Ontvang 5 munten van een speler naar keuze als het jouw beurt is','6_TV-Station',[6],5,'kies','gebouw'))
		
		for i in range(self.Horeca_aantal):
			self.cafe_l.append(Spelkaart('Cafe',2,'Ontvang 1 munt van iedere speler die dit getal gooit','3_Cafe',[3],1,'koffie','horeca'))
			self.restaurant_l.append(Spelkaart('Restaurant',3,'Ontvang 2 munten van iedere speler die dit getal gooit','X10_Restaurant',[9,10],2,'koffie','horeca'))
		
	
		# representeer de voorraad als een dict
		self.voorraad_sk = dict(zip(self.spelkaart_namen,self.spelkaart_lijsten))
		self.voorraad_dk = dict(zip(self.doelkaart_namen,self.doelkaart_lijst))
		# maak een translatie tabel voor verkorte namen als een dict
		self.korte_namen_sk = dict(zip(self.spelkaart_namen_kort,self.spelkaart_namen))
		self.korte_namen_dk = dict(zip(self.doelkaart_namen_kort,self.doelkaart_namen))
		
	def vankortnaarlangeNamen(self, korte_naam):
		if korte_naam in self.korte_namen_sk:
			return self.korte_namen_sk[korte_naam]
		if korte_naam in self.korte_namen_dk:
			return self.korte_namen_dk[korte_naam]
	
	def lijstfilenamenSpelkaarten(self):
		lijst_filenamen = []
		for spelkaart_naam in self.spelkaart_namen:
			if len(self.voorraad_sk[spelkaart_naam]) > 0:
				lijst_filenamen.append(self.voorraad_sk[spelkaart_naam][0].toonFilenaam())
		return lijst_filenamen
		
	def lijstvoorraadSpelkaarten(self):
		lijst_spelkaarten = []
		for spelkaart_naam in self.spelkaart_namen:
			naam_aantal_str = spelkaart_naam + ' ' + str(len(self.voorraad_sk[spelkaart_naam]))
			lijst_spelkaarten.append(naam_aantal_str)
		return lijst_spelkaarten
	
	def printvoorraadSpelkaarten(self):
		print('Aantal kaarten nog in voorraad:')
		for spelkaart_naam in self.spelkaart_namen:
			print(color.BOLD, spelkaart_naam, color.END, len(self.voorraad_sk[spelkaart_naam]))
	
		
	def verkoopSpelkaart(self, spelkaart_naam):
		# er wordt een kaart uit de voorraad gehaald als er nog eentje is
		if self.kaartBeschikbaar(spelkaart_naam) == True:
			spelkaart_voor_verkoop = self.voorraad_sk[spelkaart_naam][0]	# pak de eerste van de stack om te verkopen
			self.voorraad_sk[spelkaart_naam].pop()						# verwijder een kaart van de stack
			return spelkaart_voor_verkoop
		else:
			#print spelkaart_naam , ' niet meer beschikbaar'
			pass
			
	def geefDoelkaarten(self):
		doelkaarten = []
		doelkaarten.append(Doelkaart('Treinstation',4,'Je mag met twee dobbelstenen gooien','4_Treinstation'))
		doelkaarten.append(Doelkaart('Winkelcentrum',10, 'Verhoog het aantal munten met 1 voor koffie en brood','10_Winkelcentrum'))
		doelkaarten.append(Doelkaart('Pretpark',16,'Als je dubbel gooit ben je nog een keer','16_Pretpark'))
		doelkaarten.append(Doelkaart('Radiostation', 22,'Gooi je dobbelsteen nog een keer','22_Radiostation'))
		return doelkaarten			
			
	def geefStartkaarten(self):
		startkaarten = []		
		startkaarten.append(Spelkaart('Graanveld',1, 'Ontvang 1 munt van de bank ongeacht wiens beurt',	'1_Graanveld', [1], 1, 'akkerbouw','goederen'))
		startkaarten.append(Spelkaart('Bakkerij',1, 'Ontvang 1 munt van de bank als het jouw beurt is',	'2_Bakkerij', [2,3],1, 'brood','commercieel'))
		return startkaarten
	
	def spelkaarteninbudgetSpeler(self,speler):
		spelkaarten_in_budget = []
		
		for spelkaart in self.spelkaart_namen:
			if self.kaartBeschikbaar(spelkaart) == True:
				if self.voorraad_sk[spelkaart][0].toonPrijs() <= speler.munten:
					spelkaarten_in_budget.append(self.voorraad_sk[spelkaart][0])
			else:
				#print spelkaart, " is niet meer beschikbaar!"
				pass
		return spelkaarten_in_budget
		
		
	def doelkaarteninbudgetSpeler(self,speler):
		doelkaarten_in_budget = []
		for doelkaart in self.doelkaart_namen:
			if speler.doelkaartGehaaldSpeler(doelkaart) == False and self.voorraad_dk[doelkaart].toonPrijs() <= speler.munten:
					doelkaarten_in_budget.append(self.voorraad_dk[doelkaart])
		return doelkaarten_in_budget
	
	
	
	def watkostdieKaart(self, spelkaart_naam):
		return self.voorraad_sk[spelkaart_naam][0].toonPrijs()
	
	def isDoelkaart(self, kaart_naam):
		return kaart_naam in self.doelkaart_namen
		
	def isSpelkaart(self, kaart_naam):
		return kaart_naam in self.spelkaart_namen
			
	
	def kaartBeschikbaar(self, spelkaart_naam):
		# is er nog een kaart beschikbaar in de voorraad
		if len(self.voorraad_sk[spelkaart_naam]) != 0:
			return True
		else:
			return False
	
	def aantalSpelkaarten(self):
		#  geef een overzicht van alle Spelkaarten en hoeveel er nog zijn
		for s in self.voorraad_cat:
			print(s, self.aantalSpelkaart(s))
			
	def aantalSpelkaart(self, spelkaart_naam):
		# geef van een specifieke speelkaart aan hoeveel er nog zijn
		return len(self.voorraad_sk[spelkaart_naam])
		
	def plusMunten(self, munten):
		self.munten +=	munten
			
	def minMunten(self,munten):
		if (self.munten - munten) >= 0:
			self.munten -= munten
		else:
			self.munten = 0
			
	def toonNaam(self):
		return self.naam	
		
	def aantalMunten(self):
		return self.munten	
	
	def __repr__(self):
		return '%s' % (self.voorraad_sk)

class Kaart:

	def __init__(self, naam, prijs, beschrijving, filenaam):
		self.naam = naam
		self.prijs = prijs
		self.beschrijving = beschrijving
		self.filenaam = filenaam
		
	def toonPrijs(self):
		return self.prijs
	
	def toonFilenaam(self):
		return self.filenaam
	
	def toonBeschrijving(self):
		return self.beschrijving
	
	def toonNaam(self):
		return self.naam
	
	def __repr__(self):
		return '%s %s' % (self.naam, self.beschrijving)

class Doelkaart(Kaart):

	def __init__(self, naam, prijs, beschrijving,filenaam, betaald = False):
		Kaart.__init__(self, naam, prijs, beschrijving, filenaam)		
		self.betaald = betaald
	
	def koopDoelkaart(self):
		self.betaald = True
	
	def printDoelkaart(self):
		#print(color.BOLD, self.toonNaam(), (20-len(self.toonNaam()))*' ', color.END, self.toonBeschrijving(), (90-len(self.toonBeschrijving()))*' ', 'Betaald=', self.doelkaartGehaald(), ' Prijs =', self.toonPrijs())
		print(color.BOLD, self.toonNaam(),color.END,self.doelkaartGehaald())
		
	def doelkaartGehaald(self):
		return self.betaald
	
	def __repr__(self):
		return '\n %s betaald:%s'  % (Kaart.__repr__(self), self.betaald)

class Spelkaart(Kaart):

	def __init__(self,naam, prijs, beschrijving, filenaam, nr_l, waarde, soort, categorie):
		Kaart.__init__(self, naam, prijs, beschrijving, filenaam)
		self.nr_l = nr_l
		self.waarde = waarde
		self.soort = soort
		self.categorie = categorie
		
	
	def printSpelkaart(self):
		#print(color.BOLD, self.toonNaam(), (20-len(self.toonNaam()))*' ', color.END, self.toonBeschrijving(), (90-len(self.toonBeschrijving()))*' ', self.toonNrlijst(),(10-len(str(self.toonNrlijst())))*' ','Prijs=',self.toonPrijs(), self.toonSoort())
		print(color.BOLD, self.toonNaam(),color.END)
		
	def toonSoort(self):
		return self.soort
	
		
	def toonNrlijst(self):
		return self.nr_l
		
	def toonSoort(self):
		return self.soort
	
	def toonWaarde(self):
		return self.waarde
	
	def toonCategorie(self):
		return self.categorie
	
	
	def __repr__(self):
		return '\n %s prijs:%s nr:%s ' % (Kaart.__repr__(self),self.waarde, self.nr_l)
		



	
		
		
	