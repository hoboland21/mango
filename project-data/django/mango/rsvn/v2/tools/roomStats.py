#from rsvn.models import *
#from django.db.models import Avg,Count
#from datetime import timedelta, date, time, datetime

#from django.db.models import Q
from datetime import time, date,timedelta

from rsvn.v2.tools import *
from rsvn.lists import *
from rsvn.models import *
from rsvn.v2.tools.tools import *

#===========================================
# Gather Room Statistics
#===========================================
#-------------------------------------------
# bring in a Room query and make it display ready seperated by type
#-------------------------------------------
#============================================================
#---------------------
class RoomMapper(object):
#---------------------

	#-------------------
	def __init__(self) :
	#-------------------


		self.dateStart =  date.today().isoformat()
		self.dateEnd = (date.today() + timedelta(days=10)).isoformat()
		self.room_map = []
		self.rsvnid = 0
		self.roomset = set()
		self.rsvn_rooms = []	



	#-------------------
	def load_rsvn(self,rsvn):
	#-------------------
		self.rsvn = rsvn
		self.rsvnid = rsvn.id 
		self.roomset = set()
		self.rsvn_rooms = Room.objects.filter(rsvn=rsvn).order_by("roominfo__number")
		self.dateStart = rsvn.dateIn
		self.dateEnd = rsvn.dateOut

	#-------------------
	def span_roomset(self) :
	#-------------------
		self.build_tree()
		if self.rsvnid :
			self.roomset = set()
			ris = rooms_in_span(self.dateStart,self.dateEnd)
			for rm in ris  :
				self.roomset.add(rm.roominfo)
			self.step_marker(self.roomset,"occupied") 		
		
	#-------------------
	def build_tree(self) :
	#-------------------
		self.room_map = []
		for tnd in SORT_ORDER_LIST :
			roominfo = RoomInfo.objects.filter(type=tnd).order_by("number")
			self.room_map.append({
				'head' : TYPE_NAME_DICT[tnd],
				'type' : tnd,
   			    'list': roominfo,
				 })


	#-------------------
	def step_marker(self,ri_set,value)  :
	#-------------------
		for head in self.room_map :
			for ri in head['list'] :
				if ri in ri_set :
					setattr(ri,value,True)


	#-------------------
	def room_marker(self,room_list,value)  :
	#-------------------
		for head in self.room_map :
			for ri in head['list'] :
				try:
					rm = room_list.get(roominfo=ri)
					setattr(ri,value,rm.rsvn.id)	
					setattr(ri,"rsvn",rm.rsvn.id)	

				except:
					pass 

#============================================================

 