

from rsvn.models import *


import rsvn.v2.tools.tools

from rsvn.v2.tools.roomStats import *

from datetime import time, date, timedelta
from django.db.models import Q
#=====================================================================
class newGridView(object)	 :
#=====================================================================

	#----------------------------
	def __init__(self,request):
	#----------------------------
		self.header_list = ["Standard","Deluxe","Pool Deluxe","Manor","Suites" ]
		self.numDays = 24		

		self.rimap = RoomMapper()

		self.todayMark = date.strftime(date.today(),"%a%n%m/%d")
		self.dateStart = datetime.strptime(request.session['dateStart'],"%Y-%m-%d")
#		self.dateStart = datetime.strptime("2017-12-20","%Y-%m-%d")
		self.dateEnd = (self.dateStart + timedelta(days=self.numDays))

		self.dStart = self.dateStart.date()
		self.dEnd = self.dateEnd.date()

		self.roomListing = tools.rooms_in_span(self.dateStart, self.dateEnd)
		self.load_map()

	#----------------------------
	def load_map(self) :
	#----------------------------
		self.rimap.build_tree()
		for rim_head in self.rimap.room_map :
			for rio in rim_head['list'] :
				rio.cells =  [[] for i in range(self.numDays)]
				if  self.roomListing.filter(roominfo=rio) :
					rio.rooms = {}
					for rls in self.roomListing.filter(roominfo=rio) :
						rls.dateIn = max(rls.rsvn.dateIn, self.dStart)
						rls.dateOut =  min(rls.rsvn.dateOut, self.dEnd)
						rls.scheme = Scheme.objects.get(rsvn__id=rls.rsvn.id)
						rio.rooms.update({rls.id: rls})
						self.unwind(rls,rio.cells)
		self.dateSequenceX()
	
	#-------------------------------------------------------------
	def dateSequenceX(self) :
	#-------------------------------------------------------------
		self.seq = []
		for cnt in range(self.numDays) :
			thisDate = 	(self.dStart + timedelta(days=cnt))
			self.seq.append([thisDate.isoformat(),date.strftime(thisDate,"%a%n%m/%d")])


	#----------------------------
	def unwind(self,room,cells) :
	#----------------------------
		offset= room.dateIn - self.dStart
		counter = room.dateOut - room.dateIn 
		payload = self.pack_payload(room)
		for x in range(counter.days) :
			cells[x+offset.days].append(payload)

	#----------------------------
	def pack_payload(self,room)	:
	#--------------------.firstname	room.rsvn.lastname)	result = {}
		result = {}
		result["gridcolor"] = room.scheme.gridColor
		result["rsvn"] = room.rsvn.id
		result["title"] = "{}{}".format(room.rsvn.firstname,room.rsvn.lastname) 
		return result