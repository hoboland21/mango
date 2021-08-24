from rsvn.v2.tools.tools import *
from rsvn.v2.tools.vclass import VClass
from time import clock
from datetime import date,timedelta,datetime 
from copy import deepcopy
	#------------------
	def roomscan(self):
	#------------------
		self.rg1 = RGNew(self.request)
		self.result["rg1"] = self.rg1
		roomlist = self.rg1.roomlister()
		for rl in roomlist :
			rl["vacant"] = []
			rl["occupied"] = []
			for item in rl["list"] :
				if item.current == 0 :
					rl["vacant"].append(item)
				else :
					rl["occupied"].append(item)		
					
		self.result["roomlist"] = roomlist





CLEAN 		= 0
OCCUPIED 	= 1
DIRTY 		= 2
SCHED 		= 3
OOC			= 4
BB			= 5
ATTN		= 6

#==============================================================
# This is our housekeeping grid class
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class currentView(object) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#-------------------------------------------
	#-------------------------------------------
	def __init__(self) :
		self.result['tableTitle'] = "Current Room Status Information"
		self.today = datetime.today().date()
	
		# get room objects for today time frame
		# rObjs give us room information edited by staff
		self.rInfoAll = RoomInfo.objects.all()



		self.rObjs = Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(
			rsvn__status__exact='cancel') 

		# Set the roomSelect variable
		if self.arg_check('roomSelect') :
			self.roomSelect =  self.args_put['roomSelect']
			self.result['roomSelect'] = self.roomSelect 
		# grab our room object(s) and roomInfo


	

		pass
	#-------------------------------------------
	#-------------------------------------------


	#-------------------------------------------
	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
	#-------------------------------------------
		self.result['tableTitle'] = "Current Room Status Information"
		self.today = datetime.today().date()
		
		# get room objects for today time frame
		# rObjs give us room information edited by staff
		self.rInfoAll = RoomInfo.objects.all()



		self.rObjs = Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(
			rsvn__status__exact='cancel') 

		# Set the roomSelect variable
		if self.arg_check('roomSelect') :
			self.roomSelect =  self.args_put['roomSelect']
			self.result['roomSelect'] = self.roomSelect 
		# grab our room object(s) and roomInfo


			#Loading up our rooms
			roomSelectObjs= self.rObjs.filter(roominfo__number=self.roomSelect).order_by('rsvn__dateIn')
			self.targetRooms = []
			# tweek checkin/checkout 
			if len(roomSelectObjs) == 1:
				# safe to do checkin
				rso = roomSelectObjs[0]
				if self.arg_check("ciButton") :
					ro = Room.objects.get(rsvn__id = rso.rsvn.id, roominfo__number=self.args_put["ciButton"])
					ro.roomstatus = "checkin"
					ro.save()
				if self.arg_check("coButton") :
					ro = Room.objects.get(rsvn__id = rso.rsvn.id, roominfo__number=self.args_put["coButton"])
					ro.roomstatus = "checkout"
					ro.save()


			for rso in roomSelectObjs :
				rso.roomset = rso.rsvn.room_set.all() 
				for rs in rso.roomset :
					self.targetRooms.append(rs.roominfo.number)
				rso.roomcnt = len(rso.roomset)

			self.result['roomObjs'] = roomSelectObjs 


			self.rInfo = self.rInfoAll.get(number=self.roomSelect)
			self.result['roomInfo'] = self.rInfo

		# if we are requesting a clean room change
			if self.arg_check('changeRoom') :
				self.rInfo.current = roomStateDictReverse[self.args_put['changeRoom']]
				self.rInfo.save()

		self.makeGrid()


#-------------------------------------------
	def makeGrid(self) :
#-------------------------------------------
		roomList,errorList = self.updateGridInfo()
		rInfoList = []
		# we need room select associated rooms
		for name in SORT_ORDER_LIST :
			rInfoList.append("<tr><th>{}</th></tr><tr><td>".format(name[1]))
			# we are building grid cells here
			for t in self.rInfoAll.filter(type__exact=name[0]).order_by('number'):

				borderMark = errorList[t.number]
				
				# Check the rObjs__room__number and mark it green 



				if self.arg_check('roomSelect'):
					if t.number == self.roomSelect :
						borderMark += " Selected" 
					if t.number in self.targetRooms :
						borderMark += " ID_FLAG"	
				rInfoList.append("<button value='{0}' name='roomSelect' class='tcel {1} {2}' >{0}</button>".format(
					t.number,roomList[t.number],borderMark))
			
			rInfoList.append("</td></tr>")

		
#-------------------------------------------
	def back2back_check(self,rObjs,ri) :
#-------------------------------------------
		current = ri.currentText()

		if current not in [ "CLEAN", "OOC", "SCHED"] :
			current = "DIRTY"
			ri.current= DIRTY
			ri.save()
		
		for ro in rObjs :
			if ro.roomstatus == "checkin" and ri.current not in [ OOC ]:
				ri.current= OCCUPIED
				ri.save()
				current = "OCCUPIED"
		return current
#-------------------------------------------
	def updateGridInfo(self) :
#-------------------------------------------
		# fill roomlist our work list
		roomList = {}
		errorList = {}
		# we load our work list here
		for ri in self.rInfoAll :
			# load current rInfo value (using text) 
			roomList[ri.number] = ri.currentText()
			## NEW added errorList 
			errorList[ri.number] = ""
			# grab reservation object(s) for this rtoom
			rObjs = self.rObjs.filter(roominfo__number=ri.number )
			

			# if length is greater than 1 this is a back to back 
			if len(rObjs) > 1 :
				# mark it and go
				errorList[ri.number] = "BB_FLAG"
				# return room list value
				roomList[ri.number] = self.back2back_check(rObjs,ri)

			elif  len(rObjs) == 0 and roomList[ri.number] == "OCCUPIED":	
				roomList[ri.number] = "CLEAN"
				ri.current = CLEAN
				ri.save()

			# if only a single reservation applying	

			elif  len(rObjs) == 1 :
				#we seperate to one Room object focused on
				rn = rObjs[0]
				#Checking for errors
				if rn.rsvn.status in [ "checkin", "checkout"] :
					if rn.roomstatus != rn.rsvn.status :
						errorList[ri.number] = "ERROR_FLAG"	
						#print ("DEBUG Room",ri.number," - ",rn.roomstatus," - ",rn.rsvn.status)

				if rn.roomstatus == "checkin" :
					# this overrides everything and occupies the room
					roomList[ri.number] = "OCCUPIED"
					ri.current = OCCUPIED
					ri.save()

				# if the room is checked out and occupied make it dirty
				elif rn.roomstatus == "checkout" and ri.current not in [OOC,SCHED,CLEAN] :
					# checkout without any changes 
					roomList[ri.number] = "DIRTY"
					ri.current =  DIRTY
					ri.save()

		return roomList,errorList

#-------------------------------------------
	def updateState(self,number,value) :	
#-------------------------------------------
		rInfo = RoomInfo.objects.get(number = number)
		rInfo.current = value
		if self.request.user.has_perm('rsvn.delete_rsvn') :
			rInfo.save()

		
	