
from rsvn.models import *

from rsvn.vc.vclass import VClass
from time import clock
from datetime import date,timedelta,datetime 
from rsvn.vc.grid import TypeNameList
from copy import deepcopy


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
class currentView(VClass) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#-------------------------------------------
	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
	#-------------------------------------------

		self.template_name = "revise/current.html"
		self.result['tableTitle'] = "Current Room Status Information"
		self.today = datetime.today().date()
		
		# get room objects for today time frame
		# rObjs give us room information edited by staff
		self.rInfoAll = RoomInfo.objects.all()



		self.rObjs = Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(
			rsvn__status__exact='cancel') 

		print(self.args_put)
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
		for name in TypeNameList :
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

		self.result['rInfoList'] = rInfoList

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
				if rn.roomstatus != rn.rsvn.status :
					errorList[ri.number] = "ERROR_FLAG"	

				if rn.roomstatus == "checkin" :
					# this overrides everything and occupies the room
					roomList[ri.number] = "OCCUPIED"
					self.updateState(ri.number,OCCUPIED)

				# if the room is checked out and occupied make it dirty
				elif rn.roomstatus == "checkout" and ri.current not in [OOC,SCHED,CLEAN] :
					# checkout without any changes 
					roomList[ri.number] = "DIRTY"

		return roomList,errorList

#-------------------------------------------
	def updateState(self,number,value) :	
#-------------------------------------------
		rInfo = RoomInfo.objects.get(number = number)
		rInfo.current = value
		if self.request.user.has_perm('rsvn.delete_rsvn') :
			rInfo.save()

		
		
	
"""
	#-------------------------------------------
	def update_to_present(self) :
	#-------------------------------------------
		# fill roomlist our work list
		roomList = {}
		
		# we load our work list here
		for ri in self.rInfo :
			roomList[ri.number] = ri.current

		# BUILDING a duplicate for reference 
		startList = deepcopy(roomList)


		# start off by clearing all occupied rooms to vacant rooms
		# We have the duplicate to back us up
		for rl in roomList :
			if roomList[rl] == OCCUPIED :
				roomList[rl] = VACANT

		# We do it in one pass
		roomObjs = Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(rsvn__status__exact='cancel') 
		for rn in roomObjs :
			number = rn.roominfo.number
		# get all occupied rooms and set occupied
			if rn.roomstatus == "checkin" :
				roomList[number] = OCCUPIED
		# see if it has been checked out 
			if rn.roomstatus == "checkout" :
				# if checkout is today or before mark it dirty
				roomList[number] = VACANT
				if rn.rsvn.dateOut >= self.today :
					roomList[number] = DIRTY



#		# get all checked rooms
#		for rn in Room.objects.filter(rsvn__dateOut__exact = self.today,rsvn__status__exact = "checkout" ).exclude(rsvn__status__exact='cancel')  :
#			number = rn.roominfo.number
#				roomList[number] = DIRTY

		# compare rooms
		for rL in roomList :
			ri = RoomInfo.objects.get(number__exact = rL)
			if ri.current != roomList[rL] :
				ri.current = roomList[rL]
				ri.save()

		#self.logSet()
		



	{% if  roomSelect %}
		<span> Room {{ roomSelect }} Information comes here </span>

		{% csrf_token %}
		<select class='{{ roomState }}' name="roomStateChange" onChange= "this.form.submit()">
			<option value=1 {% if roomState == 'OCCUPIED' %} SELECTED {% endif %} class='OCCUPIED'>Occupied</option>
			<option value=2 {% if roomState == 'DIRTY' %} SELECTED {% endif %} class='DIRTY'>Dirty</option>
			<option value=3  {% if roomState == 'SCHED' %} SELECTED {% endif %} class='SCHED'>Sched for Cleaning</option>
			<option value=4  {% if roomState == 'OOC' %} SELECTED {% endif %} class='OOC'>Out of Comission</opyion>
			<option value=0  {% if roomState == 'CLEAN' %} SELECTED {% endif %} class='CLEAN'>Clean and Vacant</option>
			<option value=5  {% if roomState == 'BB' %} SELECTED {% endif %} class='BB'>Back to Back</option>
		</select>
		
		<button>View Reservation</button> 
		<input type='hidden' name='roomSelect' value='{{ roomSelect }}'>
	{% endif %}
	</div>





# Keep original grid
#-------------------------------------------
	def makeGrid(self) :
#-------------------------------------------
		self.rInfo = RoomInfo.objects.all()
		rInfoList = []
		for name in TypeNameList :
			tlist = self.rInfo.filter(type__exact=name[0]).order_by('number')
			rInfoList.append("<tr><th>{}</th></tr><tr><td>".format(name[1]))
			# we are building grid cells here
			for t in tlist:
				# let's affect the border here
				bgcolor = self.colorWheel[t.current]
				fgcolor = 'black'

				if bgcolor in ['black','red'] :
					fgcolor = 'yellow'
				rInfoList.append("<button value='{1}' name='toggleRoom' class='tcel' style='background-color:{0}; color:{2}' >{1}</button>".format(bgcolor,t.number,fgcolor))

			rInfoList.append("</td></tr>".format(name[1]))
		self.result['rInfoList'] = rInfoList



#-------------------------------------------
	def viewArchive(self) :
#-------------------------------------------

		currentLog =CurrentLog.objects.get(pk__exact = self.args_put['archive'])

		archiveList = currentLog.log.split(',') 

		archiveDict = {}

		for al in archiveList :
			if ":" in al :
				key,val = al.split(" : ")
				val = val.strip(",")
				archiveDict[key] = val
		
		self.rInfo = RoomInfo.objects.all()
		rInfoList = []

		for name in TypeNameList :
			tlist = self.rInfo.filter(type__exact=name[0]).order_by('number')
			rInfoList.append("<tr><th>{}</th></tr><tr><td>".format(name[1]))
			for t in tlist:
				acurrent = archiveDict[t.number]

				bgcolor = self.colorWheel[int(acurrent)]
				fgcolor = 'black'

				if bgcolor in ['black','red'] :
					fgcolor = 'yellow'
				rInfoList.append("<button value='{1}' name='toggleRoom' class='tcel' style='background-color:{0}; color:{2}' >{1}</button>".format(bgcolor,t.number,fgcolor))

			rInfoList.append("</td></tr>".format(name[1]))
		self.result['rInfoList'] = rInfoList
			

	#-------------------------------------------
	def currentReset(self) :
	#-------------------------------------------
		for ri in self.rInfo :
			if ri.current not in [ OOC, VACANT ] :
				ri.current = VACANT
				ri.save()


	#-------------------------------------------
	def clicker(self,number) :
	#-------------------------------------------
		rInfo = RoomInfo.objects.get(number = number)
		curr = rInfo.current

		curr = (curr + 1) % len(self.colorWheel)
		rInfo.current = curr
		if self.request.user.has_perm('rsvn.delete_rsvn') :
			rInfo.save()

	#-------------------------------------------
	def logSet(self) :
	#-------------------------------------------
		logList = [] 

		for ri in self.rInfo :
			logList.append("{} : {},".format(ri.number,ri.current))

		log = "".join(logList)
		thisDate = date.today().isoformat()

		currentLog =CurrentLog.objects.filter(date__exact = thisDate)

		if currentLog :
			currentLog =CurrentLog.objects.get(date__exact = thisDate)
			currentLog.log = log
		else :	
			currentLog = CurrentLog(date=thisDate, log=log)

		currentLog.save()

"""