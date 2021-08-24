from rsvn.models import RoomInfo, Rsvn, Room, Scheme
from rsvn.tools.rc import *
from rsvn.tools.rc1 import *
from datetime import timedelta, date, time, datetime


VACANT_ROOM = 0
OCCUPIED_ROOM = 1
DIRTY_ROOM = 2
CLEANING_ROOM =3
OOC_ROOM = 4


TOTAL_ROOMS = 70


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class AvailabilityGrid(object) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	result = {}
	type_available = {}
	#-------------------------------------------
	def __init__(self,start,end) :
	#-------------------------------------------
		self.start 			= start
		self.end 			=  end
		self.dateStart = datetime.strptime(self.start,"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.end,"%Y-%m-%d")
		self.aList = {}

		self.dateSpan = (self.dateEnd - self.dateStart).days + 1
		self.rsvn_list()
		self.dateScan()
		self.initialize_grid()
		
		self.deployGrid()

		self.result = {'dateStart':self.start,'dateEnd':self.end }
		self.result['globalGrid']  =  self.gM.HTML()
	#-------------------------------------------
	def  rsvn_list(self) :
	#-------------------------------------------
		self.rlist = Rsvn.objects.filter(
			Q(dateIn__gte = self.dateStart,   dateIn__lt= self.dateEnd  )   |
			Q(dateOut__gt = self.dateStart,  dateOut__lte= self.dateEnd  )  |
			Q(dateIn__lte = self.dateStart,   dateOut__gte= self.dateEnd  )
			).exclude(status__exact='cancel')
		for type in SortOrderDict :
			rooms = RoomInfo.objects.filter(type__exact=type).exclude(current__exact=OOC_ROOM)
			self.type_available[type] = len(rooms)			
	#-------------------------------------------
	def  dateSlice(self,thisDate) :
	#-------------------------------------------
		# I could extend the dateOut comparison for one day to compensate for 
		# dirty room on checkout day
		self.aList[thisDate] = {}
		#initialize our dict
		for so in SortOrderDict :
			self.aList[thisDate][so]= { 'a':0, 'ua' : 0 }
		# step through reservations and rooms 
		day_rlist = self.rlist.filter(dateIn__lte = thisDate, dateOut__gt = thisDate)
		
		for r in day_rlist :
			rooms = Room.objects.filter(rsvn__id__exact = r.id)
			assigned_rooms = len(rooms)
			unassigned_rooms = r.rooms - assigned_rooms
			# add up unassigned rooms first
			if unassigned_rooms :
				self.aList[thisDate][r.type]['ua'] += unassigned_rooms
			if assigned_rooms :
				for room in rooms :
					self.aList[thisDate][room.roominfo.type]['a'] += 1
	#-------------------------------------------
	def dateScan(self) :
	#-------------------------------------------
	# Loop through our date slices
		for offset in range(self.dateSpan) :
			thisDate = (self.dateStart + timedelta(days=offset)).date().isoformat()
			self.dateSlice(thisDate)
	#---------------------------------------------------------
	def initialize_grid(self) :
	#---------------------------------------------------------
		self.xLabels = []
		self.xLabels.append("")
		# put the date search labels in
		for offset in range(self.dateSpan) :
			self.xLabels.append((self.dateStart + timedelta(days=offset)).date().isoformat())
		# first cell is blank

		self.yLabels = []
		self.yLabels.append("")

		# by stepping through SortOrderDict - it is sorted
		for type in SortOrderDict :
				self.yLabels.append(type)

		self.gM = GridMatrix(self.xLabels,self.yLabels)
#---------------------------------------------------------
	def label_upgrade(self) :
#---------------------------------------------------------
		# replace the dates with a short date f
		for u in self.gM.xDict :
			if u != "" :
				thisDate = datetime.strptime(u,"%Y-%m-%d").date()
				newFormat = datetime.strftime(thisDate,"%m/%d")
				val = self.gM.xDict[u]
				self.gM.gridList[val][0]["data"] = newFormat
				self.gM.gridList[val][0]["color"] = "yellow"

				if thisDate == date.today() :
					self.gM.gridList[val][0]["color"] = "Green"
					self.gM.gridList[val][0]["style"] = "font-size:12pt"
		for u in self.gM.yDict :
			if u != "":
				val = self.gM.yDict[u]
				self.gM.gridList[0][val]["data"] = TypeNameDict[u]
				self.gM.gridList[0][val]["color"] = "yellow"
		
	#---------------------------------------------------------
	def deployGrid(self) :
	#---------------------------------------------------------
		self.label_upgrade()
		for thisDate in self.aList :
			for aType in self.aList[thisDate] :

				# calculate assigned and unassigned
				assigned = self.aList[thisDate][aType]['a']
				unassigned = self.aList[thisDate][aType]['ua']
				data = self.type_available[aType]-assigned-unassigned
				self.gM.put('data',thisDate,aType,data)


#==============================================================
# This is our housekeeping grid class
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class BRC(object) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	colorWheel = ['white','red','gray', 'yellow','black']

	def __init__ (self) :
		self.today  	= date.today()
		self.yesterday  = self.today-timedelta(days=1)
		# get all the rooms
		self.roomInf = RoomInfo.objects.all()
#		self.update_to_present()
#		self.roomInf = RoomInfo.objects.all()


	#-------------------------------------------
	def roomGrid(self):
	#-------------------------------------------
		code = []
		for heading in SortOrderDict :
			code.append("<tr><th>{}</th></tr>".format(TypeNameDict[heading]))
			code.append("<tr><td>")
			rinf = self.roomInf.filter(type__exact=heading)
			for q in  rinf.order_by('number'):
				marker = q.current
				room = q.number

				style = self.buildStyle(q)
				code.append("<button class='{0} roomButton' name='roomSelect'  style='{2}' \
								value='{1}' > {1}</button>".format(marker,room,style))

			code.append("</td></tr>")
		return code


	#-------------------------------------------
	def scan_checkout(self) :
	#-------------------------------------------
	# This one is executed for every entry into the BRC
	#--------------------------------------------------
		# our work list
		roomList = {}

		# our changed worklist values

		changed_roomList = {}

		for ri in self.roomInf :
			roomList[ri.number] = ri.current
		# filter all current rooms
		currentRooms = Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today).exclude(rsvn__status__exact='cancel') 
		# here we switch Occupied rooms to dirty rooms
		for rn in currentRooms.filter(rsvn__status__exact = "checkout" ) :
			number = rn.roominfo.number
			if roomList[number] in [ OCCUPIED_ROOM ] :
				changed_roomList[number] = DIRTY_ROOM

		# get all checked in rooms and set occupied
		for rn in currentRooms :
			number = rn.roominfo.number
			if rn.rsvn.status == "checkin" :
				changed_roomList[number] = OCCUPIED_ROOM
			elif rn.roominfo.current == OCCUPIED_ROOM:
				changed_roomList[number] = VACANT_ROOM

		# compare rooms
		for rL in changed_roomList :
			ri = RoomInfo.objects.get(number__exact = rL)
			ri.current = changed_roomList[rL]
			ri.save()
	#-------------------------------------------
	def update_to_present(self) :
	#-------------------------------------------
		roomList = {}
		for ri in self.roomInf :
			roomList[ri.number] = ri.current

		# start off by clearing all occupied rooms to vacant rooms
		for rl in roomList :
			if roomList[rl] == OCCUPIED_ROOM :
				roomList[rl] = VACANT_ROOM

		# get all occupied rooms and set occupied
		for rn in Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(rsvn__status__exact='cancel') :
			number = rn.roominfo.number
			if rn.rsvn.status == "checkin" :
				roomList[number] = OCCUPIED_ROOM

		# get all checked rooms
		for rn in Room.objects.filter(rsvn__dateOut__exact = self.today,rsvn__status__exact = "checkout" ).exclude(rsvn__status__exact='cancel')  :
			number = rn.roominfo.number
			if roomList[number]  in [ VACANT_ROOM,OCCUPIED_ROOM ] :
				roomList[number] = DIRTY_ROOM

		# compare rooms
		for rL in roomList :
			ri = RoomInfo.objects.get(number__exact = rL)
			if ri.current != roomList[rL] :
				ri.current = roomList[rL]
				ri.save()



	#-------------------------------------------
	def currentReset(self) :
	#-------------------------------------------
		for ri in self.roomInf :
			if ri.current != OOC_ROOM :
				ri.current = 0
			ri.save()

	#-------------------------------------------
	def buildStyle(self,roominfo) :
	#-------------------------------------------
		styling = []
		fgColor = "black"
		bgColor = self.colorWheel[roominfo.current]
		if bgColor in ['black','Black'] :
			fgColor = 'yellow'
		styling.append("background-color:{}; color:{}".format(bgColor,fgColor))

		return " ".join(styling)
	#-------------------------------------------
	def clicker(self,number) :
	#-------------------------------------------
		rInfo = RoomInfo.objects.get(number = number)
		curr = rInfo.current

		curr = (curr + 1) % len(self.colorWheel)
		rInfo.current = curr
		if self.user.has_perm('rsvn.delete_rsvn') :
			rInfo.save()

