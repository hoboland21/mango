from rsvn.tools.misc import *
from rsvn.models import *

from django.views.generic.base import View
from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

from rsvn.vctools.tools import *

from rsvn.vctools.newGrid import *
from rsvn.vc.vclass import VClass

from django.utils import timezone
import pytz

#=====================================================================
class ServiceView (VClass)	 :
#=====================================================================

	start = date.today()
	end = date.today()

	ServiceLabels ={
		'from_airport'	: 'From Airport Trans',
		'to_airport'	: 'To Airport Trans',
		'earlyin'		: 'Early Check In',
		'lateout' 		: 'Late Check Out',
		'connect' 		: 'Connecting Room',
		'dailymaid'		: 'Daily Maid Service',
		'extrabed'		: 'Extra Bed',
		'mango' 		: 'Mango Access',
		'breakfast'		: 'Breakfast',
		'crib'			: 'Baby Crib'
		}

	ServiceLabelsList =[
		['breakfast'	, 'Breakfast'],		
		['from_airport'	, 'From Airport Trans'],
		['to_airport'	, 'To Airport Trans'],
		['mango' 		, 'Mango Access'],
		['earlyin'		, 'Early Check In'],
		['lateout' 		, 'Late Check Out'],
		['connect' 		, 'Connecting Room'],
		['dailymaid'	, 'Daily Maid Service'],
		['extrabed'		, 'Extra Bed'],
		['crib'			, 'Baby Crib'],
		]
				
	# ---------------
	def main(self) :
	# ---------------
		self.template_name = "revise/service.html"
		self.result['tableTitle'] = "Service Schedule Table"

		self.args = { 
			"dateStart"	:  date.today().isoformat(),
			"dateEnd"	:  (date.today() + timedelta(days=10)).isoformat(),
		}
		self.args_fix()
		# date controller

		self.dateStart = datetime.strptime(self.args['dateStart'],"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.args['dateEnd'],"%Y-%m-%d")

		self.numDays = (self.dateEnd - self.dateStart).days+1
		
		self.GM = gridMatrix()	
		self.GM.dateSequenceX(self.dateStart,days=self.numDays, format="%m/%d")
		self.GM.loadY(self.ServiceLabelsList)
		# mark date heading for 
		if self.dateStart.date() <= datetime.today().date() and  self.dateEnd.date() >= datetime.today().date() :
			self.GM.gridList[self.GM.xDict[datetime.today().date().isoformat()]][0]['color'] = "green"

		self.rsvn_select()
		self.serviceMake()

		self.result['Sgrid'] = self.GM.HTML()

		self.args_send()
	#-------------------------------------------------------
	def serviceMake(self) :
	#-------------------------------------------------------
		for offset in range(self.numDays) :
			thisDate = (self.dateStart + timedelta(days=offset)).date()

			thisDateStr = thisDate.isoformat()
			dailyS = {}
			
			# indicate for each day of the reservation


			breakfast 				= self.rsvnListing.filter(service__breakfast__exact=True,dateOut__gte=thisDate,dateIn__lt=thisDate)
			roomcnt = 0
			for brk in breakfast :
				roomcnt += brk.child
				roomcnt += brk.adult


			dailyS['breakfast'] 	= roomcnt
			dailyS['mango']			= len(self.rsvnListing.filter(service__mango__exact=True,dateOut__gte=thisDate,dateIn__lte=thisDate))			
			dailyS['connect']		= len(self.rsvnListing.filter(service__connect__exact=True,dateOut__gte=thisDate,dateIn__lte=thisDate))			
			dailyS['dailymaid']		= len(self.rsvnListing.filter(service__dailymaid__exact=True,dateOut__gt=thisDate,dateIn__lt=thisDate))			
			
			# only one day is important		
			dailyS['from_airport'] 	= len(self.rsvnListing.filter(service__from_airport__exact=True,dateIn__exact=thisDate))
			dailyS['to_airport'] 	= len(self.rsvnListing.filter(service__to_airport__exact=True,dateOut__exact=thisDate))
			dailyS['earlyin']		= len(self.rsvnListing.filter(service__earlyin__exact=True,dateIn__exact=thisDate))			
			dailyS['lateout']		= len(self.rsvnListing.filter(service__lateout__exact=True,dateOut__exact=thisDate))			
			dailyS['extrabed']		= len(self.rsvnListing.filter(service__extrabed__exact=True,dateIn__exact=thisDate))			
			dailyS['crib']			= len(self.rsvnListing.filter(service__crib__exact=True,dateIn__exact=thisDate))			

			for ds in dailyS :
				data = 0
				if dailyS[ds] > 0:
					data = dailyS[ds] 
				self.GM.put('data',thisDateStr,ds,data)

										
	#-------------------------------------------
	def rsvn_select(self):
	#-------------------------------------------
		self.rsvnListing = Rsvn.objects.filter(
			Q(dateIn__gte = self.dateStart,   dateIn__lt= self.dateEnd  )   |
			Q(dateOut__gt = self.dateStart,  dateOut__lte= self.dateEnd  )  |
			Q(dateIn__lte = self.dateStart,   dateOut__gte= self.dateEnd  )
			).exclude(status__exact='cancel')



