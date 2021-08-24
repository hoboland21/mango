from rsvn.models import *
from datetime import date,timedelta,datetime
from django.db.models import Q
from rsvn.vctools.packing import *
from decimal import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Calcs(object) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	OCCUPANCY_TAX = Decimal('0.15')
	

	#-------------------------------------------
	def __init__(self) :
	#-------------------------------------------
		self.rateHeading = "Tour FIT"
		self.calculation = {}
		
	#-------------------------------------------
	def loadRsvn(self,rsvnid) :
	#-------------------------------------------
		self.rsvnid = int(rsvnid)
		self.rsvn  = Rsvn.objects.get(pk=self.rsvnid)
		self.dateIn = self.rsvn.dateIn
		self.dateOut = self.rsvn.dateOut
		self.rateType 	= self.rsvn.type
		title= RATEHEADING_DEFAULT_DICT[self.rsvn.source] 
		
		# if this is a tour we better check for special tour price
		if Tour.objects.filter(rsvn__exact = self.rsvn.id) :
			agentRate = AgentRate.objects.get(agent__tour__rsvn__exact = self.rsvn.id)
			self.rateHeading = agentRate.rateheading
		else:
			self.rateHeading =RateHeading.objects.get(title__exact=title) 
		
		self.seasonCheck()
		self.roomCalculate()
							
	#-------------------------------------------
	def roomCalculate(self) :
	#-------------------------------------------
		self.rateAtom = RateAtom.objects.get(rateheading__exact=self.rateHeading.id,rateType__exact = self.rateType)
		
		rateval = {
			'low': Decimal(self.rateAtom.lowSeason),
			'high': Decimal(self.rateAtom.highSeason),
			'peak': Decimal(self.rateAtom.peakSeason),
		}
		room_charge = Decimal('0')
		
		self.calculation['roomCharge'] = []

		for sea in self.season :
			block = {}
			block['name'] = sea.name
			block['nights'] = sea.nights 
			block['rate'] = Decimal(rateval[sea.season])
			block['total'] =  sea.nights * block['rate']
			self.calculation['roomCharge'].append(block) 
			room_charge += block['total']
		
		self.calculation['totalRoomCharge'] = room_charge		

		self.calculation['Tax'] = Decimal(room_charge) * self.OCCUPANCY_TAX


		self.serviceCalculate()


	#-------------------------------------------
	def serviceCalculate(self) :
	#-------------------------------------------
		self.serviceRate = RateAtom.objects.filter(rateheading__title__exact = "SERVICE")
		self.calculation['service'] = []

		if self.rsvn.service_set.all() :
			self.serviceList  = serviceSplitter(self.rsvn.service_set.all()[0])

			for serv in self.serviceList :
				name = serv[1]
				dbname = serv[0]
				block = {}
				rate = self.serviceRate.get(rateName__exact = name)
				block['name'] = name
		
				multi = Decimal('1')

				# we do the multiple for meals and
				if dbname in [ 'breakfast','lunch','dinner', 'dailymaid'] :
					multi = Decimal(self.rsvn.num_days())
				val = multi * rate.lowSeason
				block['multi'] = multi
				block['rate'] = rate.lowSeason		
				block['total'] = val
				self.calculation['service'].append(block)				



	#-------------------------------------------
	def seasonCheck(self):
	# we grab the applicable season(s) for this rsvn.. we make a list called self.season
	# it gives us season high or low and the number of days
	#-------------------------------------------
		self.season = Season.objects.filter(
			Q(beginDate__gte = self.dateIn, beginDate__lte = self.dateOut) |
			Q(beginDate__lte = self.dateIn, endDate__gte = self.dateIn) |
			Q(beginDate__lt = self.dateOut, endDate__gte = self.dateOut)
			)
		
		for seas in self.season :
			firstday = max(seas.beginDate,self.dateIn)
			lastday = min(seas.endDate, self.dateOut)
			
			seas.nights = (lastday - firstday).days+1
			if lastday == self.dateOut :
				seas.nights += -1





