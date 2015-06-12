from rsvn.vc.vclass import VClass
from time import clock
from rsvn.models import *

from django.db.models import Q

from datetime import date,timedelta,datetime

from rsvn.vctools.newGrid  import gridMatrix
from rsvn.vctools.roomGrid import *

TypeNameCountList = [
	['standard', 		'Standard'		,27],
	['deluxe', 			'Deluxe'  		,26],
	['pool_deluxe', 	'Pool Deluxe'	,12],
	['lanai' , 			'Lanai' 		,4 ] ,
	['presidential',	'Presidential'	,1],
	['manor', 			'Manor' 		,3],
	['suites',			'Suites'		,17],
	]


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class availableView(VClass) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
		t0 = clock()
		self.template_name = "revise/available.html"
		self.result['tableTitle'] = "Room Availability Table"
		# these are session and received arguments... part of vclass
		self.args = { 
			"dateStart"	:  date.today().isoformat(),
			"dateEnd"	:  (date.today() + timedelta(days=10)).isoformat(),
		}
		self.args_fix()

		# date controller

		self.dateStart = datetime.strptime(self.args['dateStart'],"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.args['dateEnd'],"%Y-%m-%d")

		self.numDays = (self.dateEnd - self.dateStart).days+1
		
		
		# get the static room label filling self.RoomOrderList
		
		# create the grid structure		
		self.GM = gridMatrix()	
		self.GM.dateSequenceX(self.dateStart,days=self.numDays, format="%m/%d")
		self.GM.loadY(TypeNameCountList)
		self.GM.highlightDate(date.today().isoformat(),'green')
		
		# start our processing now
		self.rsvnlist()
		self.loadChart()

		# when we are completed we send the grid for rendering
		self.result['gridHTML'] = self.GM.HTML()

		# send our session arguments out
		
		self.args_send()
		
	#-------------------------------------------
	def  loadChart(self) :
	#-------------------------------------------
		# deduct OOC rooms
		self.check_ooc_rooms()

		for offset in range(self.numDays) :
			
			# initialize tally
			tally = {}
			
			for name in TypeNameCountList :
				tally[name[0]] = {'u': 0, 'a' : 0 }
			
			# calculate the date
			thisDate = self.dateStart + timedelta(days=offset)

			# get the valid reservations for this date slice
			dateSlice = self.rsvnList.filter(dateIn__lte = thisDate,dateOut__gt = thisDate)

			# analyze date slice
			for ds in dateSlice :
				assigned = len(ds.room_set.all())
				unassigned = ds.rooms - assigned
				tally[ds.type]['a'] += assigned
				tally[ds.type]['u'] += unassigned

			# load data actually
			for name in TypeNameCountList :
				data = "a:{} u:{}".format(tally[name[0]]['a'],tally[name[0]]['u'])
				total = self.typeCount[name[0]] - tally[name[0]]['a'] - tally[name[0]]['u'] 
				self.GM.put('data',thisDate.date().isoformat(),name[0],total)
				self.GM.put('title',thisDate.date().isoformat(),name[0],data)

	#-------------------------------------------
	def check_ooc_rooms(self) :
	#-------------------------------------------
		self.typeCount ={}
		for name in TypeNameCountList :
			self.typeCount[name[0]] = name[2]
		for room in RoomInfo.objects.filter(current__exact=OOC) :
			self.typeCount[room.type] -= 1 
			
	#-------------------------------------------
	def  rsvnlist(self) :
	#-------------------------------------------
		self.rsvnList = Rsvn.objects.filter(
			Q(dateIn__gte = self.dateStart,  dateIn__lt= self.dateEnd  )   |
			Q(dateOut__gt = self.dateStart,  dateOut__lte= self.dateEnd  )  |
			Q(dateIn__lte = self.dateStart,  dateOut__gte= self.dateEnd  )
			).exclude(status__exact='cancel')







