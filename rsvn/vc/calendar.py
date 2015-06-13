from rsvn.tools.misc import *
from rsvn.models import *
from django.db.models import F, Count, Sum
from django.views.generic.base import View
from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

from rsvn.vctools.tools import *
from rsvn.vctools.packing import *

from rsvn.vc.vclass import VClass

from django.utils import timezone
import pytz

# This has turned out to be the most valuable page for staff
# and daily use

#=====================================================================
class CalView (VClass)	 :
#=====================================================================
	form_class = ""
	result ={}
	request = ""
	args_put = {}
	args_get = {}
	
	#-------------------------------------------------------
	def main (self) :
	#-------------------------------------------------------
		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid
		self.template_name = "revise/calendar.html"

		self.args = { 
				"dateSelect"	:  date.today().isoformat(),
			}

		self.args_fix()
		#------------------------------------

		# establish date of concern  .. gives us self.thisDate and adjusts our 
		# date stepper
		self.fixDate()


		# scan the data base
		self.scanRoomData()
		
		self.scanRsvnData()

		self.scanEventData()

		# collate service information
		self.serviceMake(self.thisDate)

		
		self.dailyReports()
		#------------------------------------
		self.args_send()
		# send record to the header

		if int(self.rsvnid) > 0 :
			self.result['rsvnRec'] =  rsvnidPacker(self.rsvnid)
			self.result['rsvnid']  = self.rsvnid
	#-------------------------------------------------------
	def dailyReports(self) :
	#-------------------------------------------------------
		# we want to know 7 day and 30 day mark
		rsvn7 = []
		rsvn30 = []
		for CI in self.RsvnData['in_house'] :
			if CI.day_num > 0 :
				if CI.day_num % 7 == 0 :
					rsvn7.append(CI) 
				if CI.day_num % 30 == 0 :
					rsvn30.append(CI) 
		self.result['rsvn7'] = rsvn7
		self.result['rsvn30'] = rsvn30

	
			
	#-------------------------------------------------------
	def scanRoomData(self) :
	#-------------------------------------------------------
		# grab all the in Rooms Info
		self.inHouse 	= Room.objects.filter(rsvn__dateIn__lt = self.thisDate,   rsvn__dateOut__gt= self.thisDate).exclude(rsvn__status__exact='cancel')
		self.chkinRooms  = Room.objects.filter(rsvn__dateIn__exact = self.thisDate).exclude(rsvn__status__exact='cancel')		
		self.chkoutRooms = Room.objects.filter(rsvn__dateOut__exact = self.thisDate).exclude(rsvn__status__exact='cancel')			
		self.result['in_house_statlist'] 	= self.roomStats(self.inHouse)
		self.result['in_statlist'] 			= self.roomStats(self.chkinRooms)
		self.result['out_statlist'] 		= self.roomStats(self.chkoutRooms)
		self.result["calHouse"] 			= self.inHouse
	#-------------------------------------------------------
	def scanRsvnData(self) :
	#-------------------------------------------------------
		# pull out daily data
		self.RsvnData = {}
		
		self.rsvnList				= Rsvn.objects.filter(dateIn__lte = self.thisDate,   dateOut__gte= self.thisDate).exclude(status__exact='cancel')
		self.RsvnData['in_house'] 	= self.rsvnList.filter(dateIn__lt = self.thisDate,dateOut__gt= self.thisDate)
		self.RsvnData['check_in'] 	= self.rsvnList.filter(dateIn__exact = self.thisDate)
		self.RsvnData['check_out'] 	= self.rsvnList.filter(dateOut__exact = self.thisDate)


# FINISH THIS FUNCTION
		for dataset in  self.RsvnData.keys() :
			if dataset in ["check_in","check_out"] :
				for rsvn in self.RsvnData[dataset] :
					rsvn = rsvnPacker(rsvn)

				self.result[dataset] = self.RsvnData[dataset]
			dset = self.pax_rooms(self.RsvnData[dataset])
			self.result[dataset + '_pax'] = dset['total_pax']


		# I want to use annotate here
		for CI in self.RsvnData['in_house'] :

			CI = rsvnPacker(CI)
			CI.day_num = (self.thisDate - CI.dateIn).days

		# pack and ship the data
		#self.pax_rooms(self.houseRsvn)

		#self.rsvnPack()


	#-------------------------------------------------------
	def roomStats(self,query) :
	#-------------------------------------------------------
		# bring in room queryset 
		result = []
		for RT in ROOM_TYPE_CHOICES :
			jt = len(query.filter(roominfo__type__exact = RT[0]))
			if jt > 0 :
				result.append({'item' : RT[1], 'value' : jt, 'class' : RT[0] })
		
		return result
#-------------------------------------------------------
	# argument is Rsvn object query.. will return #rooms #adult #child #infant
	def pax_rooms(self,query) :
	#-------------------------------------------------------
		answer = {}
		answer.update((query.aggregate(total_adult=Sum(F('adult')))))
		answer.update((query.aggregate(total_child=Sum(F('child')))))
		answer.update((query.aggregate(total_infant=Sum(F('infant')))))
		answer.update((query.aggregate(total_rooms=Sum(F('rooms')))))
		answer.update((query.aggregate(total_pax=Sum(F('adult')) + Sum(F('child')) + Sum(F('infant'))))) 

		return answer
		

	#-------------------------------------------------------
	def scanEventData(self) :
	#-------------------------------------------------------
		# event s
		self.calEvent = Event.objects.filter(dateStart__lte = self.thisDate,dateEnd__gte = self.thisDate).exclude(rsvn__status__exact='cancel')
		for cal in self.calEvent :
				cal.roomset = cal.rsvn.room_set.all().order_by('roominfo__number')

		self.eCalEvent = SideEvent.objects.filter(dateStart__lte = self.thisDate,dateEnd__gte = self.thisDate)
		### Create eventList which contains both type with a pointer
		elist = []
		for eventGroup in [ self.calEvent, self.eCalEvent ] :
			for event in eventGroup :
				elist.append(event)

		self.result['eventList'] = elist		


	#-------------------------------------------------------
	def fixDate(self) :
	#-------------------------------------------------------
		caldate = datetime.strptime(self.args['dateSelect'],"%Y-%m-%d").date()


		self.pac_tz = pytz.timezone('Pacific/Guam')
		# set the time zone to avert insanity
		#caldate = self.pac_tz.localize(caldate)
		# our stepper on page

		if self.arg_check('datePlus') :
			caldate = (caldate + timedelta(days=1))
		if self.arg_check('dateMinus') :
			caldate =  (caldate - timedelta(days=1))

		self.thisDate = caldate
		self.result['caldate'] = caldate

		# return the date to HTML
		self.args["dateSelect"]= datetime.strftime(caldate,"%Y-%m-%d")                                                                                                                

		# This gives us the delta days in text
		dday = (date.today() - self.thisDate).days

		if dday == 1 :
			dday = " Yesterday"
		elif dday == -1 :
			dday = " Tomorrow"
		elif dday == 0 :
			dday = " Today"
		elif dday < 0 :
			dday = " %s days from now" % abs(dday)
		else :
			dday = " %s days ago" % abs(dday)

		self.result['dday'] =  dday


	#-------------------------------------------------------
	def serviceMake(self,thisDate) :
	#-------------------------------------------------------
		# This is the weekly housekeeping watch
#		weekly 	=  sorted(self.sevenCheck(thisDate))
		
#		breakfast = {}
		# Service breakdown
#		breakList = Service.objects.filter(rsvn__dateIn__lt = thisDate,  rsvn__dateOut__gte=thisDate,  breakfast__exact = True ).exclude(rsvn__status__exact='cancel')
		

		# set checkout cutoff time to 11:00 am
		cotime = time(11,0)


		checkOutDateTime = self.pac_tz.localize(datetime.combine(self.thisDate,cotime))
		

		breakfastChk	= self.rsvnList.filter(dateIn__lt = self.thisDate,dateOut__gte= self.thisDate,
												service__breakfast__exact="True"
												).exclude(dateOut__exact= self.thisDate, tour__depart_time__lt=checkOutDateTime)

		self.result['breakCount'] = self.pax_rooms(breakfastChk)



		dailyList = Service.objects.filter(rsvn__dateIn__lt = thisDate,  rsvn__dateOut__gt=thisDate,  dailymaid__exact = True ).exclude(rsvn__status__exact='cancel')

		for dl in dailyList :
			dl.roomset = dl.rsvn.room_set.all()
		
#		for dl in breakList :
#			dl.roomset = dl.rsvn.room_set.all()
		
		toAirport =	Service.objects.filter(rsvn__dateOut__exact = thisDate,to_airport__exact=True).exclude(rsvn__status__exact='cancel')
		for dl in toAirport :
			dl.roomset = dl.rsvn.room_set.all()
		
		fromAirport = Service.objects.filter(rsvn__dateIn__exact = thisDate,from_airport__exact=True).exclude(rsvn__status__exact='cancel')
		for dl in fromAirport :
			dl.roomset = dl.rsvn.room_set.all()

		# let's try aggregate here
#		self.result.update((breakList.aggregate(total_adult_breakfast=Sum(F('rsvn__adult')))))
#		self.result.update((breakList.aggregate(total_child_breakfast=Sum(F('rsvn__child')))))

		
		self.result['dailyList'] = dailyList
		self.result['toAirport'] = toAirport
		self.result['fromAirport'] = fromAirport

