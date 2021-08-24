#from rsvn.models import *
#from django.db.models import Avg,Count
#from datetime import timedelta, date, time, datetime

#from django.db.models import Q

from rsvn.v2.tools.tools import *
#===========================================
# Gather Room Statistics
#===========================================

#---------------------
class RsvnRoomStats(object):
#---------------------
	#-------------------
	def __init__(self,rsvn):
	#-------------------
		self.rsvn = rsvn
		self.rsvnid = rsvn.id 
		self.displayRooms =  []
		self.roomSet = set()
		self.rsvn_rooms = Room.objects.filter(rsvn=rsvn).order_by("roominfo__number")

	
	#-------------------
	def collect_span_rooms(self) :
#	#-------------------
		try :

			self.rsvn = Rsvn.objects.get(id=self.rsvnid)
			self.startDate = self.rsvn.dateIn
			self.endDate = self.rsvn.dateOut
			self.roomlist = Room.objects.filter(
				Q(rsvn__dateIn__gte = self.startDate,   rsvn__dateIn__lt= self.endDate  )   |
				Q(rsvn__dateOut__gt = self.startDate,  rsvn__dateOut__lte= self.endDate  )  |
				Q(rsvn__dateIn__lte = self.startDate,   rsvn__dateOut__gte= self.endDate  )
				)
			for roomq in self.roomlist :
				self.roomSet.add(roomq.roominfo)
			#	

		except : 
			print("start Date not initialized")

	#-------------------
	def roomlister(self) :
	#-------------------
		self.collect_span_rooms()
		displayRooms =  []

		#step through each occupied room, mark roominfolist
		for tnd in SORT_ORDER_LIST :
			roominfo = RoomInfo.objects.filter(type=tnd).order_by("number")
			for ri in roominfo :
				ri.hit = False
				if ri in self.roomSet :	
					ri.hit = True
			displayRooms.append({
				'head' : TYPE_NAME_DICT[tnd],
				'type' : tnd,
   			    'list': roominfo,
				 })
		# we have a set of occupied rooms	
		return displayRooms


	
	#----------------
	def mark_hits(hitlist) :
	#----------------
		for head in self.displayArray :
			for rm in head.list :
				rm.hit=False
				if rm in hitlist :
					rm.hit = True
		return self.displayArray

#---------------------
class RGNew(object) :
#---------------------
	def __init__(self,request) :
		self.rsvnid = 0
		try :
			if 'rsvnid' in request.session and request.session["rsvnid"] != 0 :
				self.rsvnid = request.session["rsvnid"]
				self.rsvn = Rsvn.objects.get(id=self.rsvnid)
				self.startDate = self.rsvn.dateIn
				self.endDate = self.rsvn.dateOut
				self.rsvn_rooms = Room.objects.filter(rsvn=self.rsvn).order_by("roominfo__number")
		except : 
			print("start Date not initialized")


	def roomlister(self) :
		displayRooms =  []
		roomSet = set()
		roomlist = Room.objects.filter(
			Q(rsvn__dateIn__gte = self.startDate,   rsvn__dateIn__lt= self.endDate  )   |
			Q(rsvn__dateOut__gt = self.startDate,  rsvn__dateOut__lte= self.endDate  )  |
			Q(rsvn__dateIn__lte = self.startDate,   rsvn__dateOut__gte= self.endDate  )
			)
		
		# remove duplicate room number

		for roomq in roomlist :
			roomSet.add(roomq.roominfo)

		#step through each occupied room, mark roominfolist
		for tnd in TYPE_NAME_DICT :
			roominfo = RoomInfo.objects.filter(type=tnd).order_by("number")
			for ri in roominfo :
				if ri in roomSet :	
					ri.current = 1
				else: 
					ri.current = 0	
			displayRooms.append({
				'head' : TYPE_NAME_DICT[tnd],
				'type' : tnd,
   			    'list': roominfo,
				 })
	
		# we have a set of occupied rooms	

		return displayRooms












