from rsvn.tools.misc import *
from rsvn.models import *

from django.views.generic.base import View
from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

#from rsvn.vctools.calClass import *
from rsvn.vctools.tools import *

from rsvn.vctools.newGrid import *

from rsvn.vc.vclass import VClass


from django.utils import timezone
import pytz

from decimal import *
		
TypeNameCountList = [
	['totalhotel',		'Total Hotel'	,27+26+12+4+1 ],
	['standard', 		'Standard'		,27],
	['deluxe', 			'Deluxe'  		,26],
	['pool_deluxe', 	'Pool Deluxe'	,12],
	['lanai' , 			'Lanai' 		,4 ] ,
	['presidential',	'Presidential'	,1],
	['suites',			'Suites'		,17],
	['manor',			'Manor'			,21]
	]

HotelNameList = ['standard','deluxe','pool_deluxe','lanai','presidential' ]

#=====================================================================
class occupancyView (VClass) :
#=====================================================================

	# ---------------
	def main(self) :
	# ---------------
		self.template_name = "revise/occupancy.html"
		
		self.result['tableTitle'] = "Occupancy"

		self.args = { 
			"dateStart"	:  date.today().isoformat(),
			"dateEnd"	:  (date.today() + timedelta(days=10)).isoformat(),
		}

		self.args_fix()
		# date controller

		self.dateStart = datetime.strptime(self.args['dateStart'],"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.args['dateEnd'],"%Y-%m-%d")
		self.numDays = (self.dateEnd - self.dateStart).days + 1
		
		
				
		# create the grid structure		
		self.GM = tableMatrix()	
		self.GM.dateSequence(self.dateStart,days=self.numDays, axis='y', format="%m/%d")
		self.GM.xLabels = TypeNameCountList
		self.GM.loadTable()


		self.GM.highlightDate(date.today().isoformat(),'green') 
	
		self.dailyHigh = ['',0]
		self.dailyLow = ['',100]
			
	
		self.dailyList()		
		self.TotalCalculation()
		
		
		self.result['gridHTML'] = self.GM.HTML()
		self.args_send()



	#-------------------------------------------
	#  dateList --[date]--[type] --[num,num,num]
	#-------------------------------------------
	def dailyList(self) :
	#-------------------------------------------
	# getcontext().prec = 5
		DayCounter = {}
		self.TotalDayCounter = {}
		for r in TypeNameCountList :
			DayCounter[r[0]] = 0
			self.TotalDayCounter[r[0]] = 0
			
		for offset in range(self.numDays) :
			thisDate = (self.dateStart + timedelta(days=offset)).date().isoformat()
			rMain    = Room.objects.filter(rsvn__dateIn__lte = thisDate, rsvn__dateOut__gt = thisDate).exclude(rsvn__status = "cancel")
			
			if rMain :
				# we get our types loaded for the day
				HotelCounter = 0
				for name in TypeNameCountList :
					cnt = len( rMain.filter(roominfo__type__exact = name[0] ) )		
					DayCounter[name[0]]  = cnt
					if name[0] in HotelNameList :
						HotelCounter += cnt
				DayCounter['totalhotel'] = HotelCounter			

				self.DailyCalculation(thisDate,DayCounter)
	
	#-------------------------------------------
	def DailyCalculation(self,thisDate,DayCounter) :
	#-------------------------------------------
		for t in TypeNameCountList :
			#update the grid with todays numbers
			
			avg = Decimal(DayCounter[t[0]]) * Decimal('100')/ Decimal(t[2]) 
			avgp =	"{}% ".format (avg.quantize(Decimal('.01')))
			
			if t[0] == 'totalhotel' :
				if avg > self.dailyHigh[1] :
					self.dailyHigh[0] = thisDate
					self.dailyHigh[1] = avg
				if avg < self.dailyLow[1] :
					self.dailyLow[0] = thisDate
					self.dailyLow[1] = avg
				
			self.GM.put('data',t[0],thisDate,avgp)
			# our total statistics 
			self.TotalDayCounter[t[0]] += DayCounter[t[0]] 
	#-------------------------------------------
	def TotalCalculation(self) :
	#-------------------------------------------
		code  = [ ]
		code.append("<tr><th>Type</th><th>Count</th><th>Occupied</th><th>Occupancy</th></tr>")
		for t in TypeNameCountList :
			total = Decimal(self.TotalDayCounter[t[0]] )
			total_rooms = Decimal(self.numDays * t[2])
			total_perc = Decimal( (total / total_rooms) * 100 ).quantize(Decimal('.01'))
			code.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}%</td></tr>".format(t[1],total_rooms,total,total_perc) )
		code.append("<tr><td style='font-weight:bold' colspan='2'>Hotel Daily High</td><td>{}</td><td>{}%</td></tr>".format(self.dailyHigh[0],self.dailyHigh[1].quantize(Decimal('.01'))))
		code.append("<tr><td style='font-weight:bold' colspan='2'>Hotel Daily Low</td><td>{}</td><td>{}%</td></tr>".format(self.dailyLow[0],self.dailyLow[1].quantize(Decimal('.01')) ))
		self.result["totals"] = ' '.join(code)






