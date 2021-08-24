from rsvn.models import RoomInfo, Rsvn, Room, Scheme
from django.db.models import Avg,Count

from datetime import timedelta, date, time, datetime

from django.db.models import Q


TypeNameDict = {
	'standard' :'Standard',	'deluxe': 'Deluxe',
	'pool_deluxe' :'Pool Deluxe',	'lanai' : 'Lanai',
	'presidential' : 'Presidential',	'manor' : 'Manor',
	'suites':'Suites','garden':'Garden'
	}

SortOrderDict =  [ 	'standard','deluxe','pool_deluxe','lanai','presidential','manor','suites','garden']

VACANT 		= 0
OCCUPIED 	= 1
DIRTY 		= 2
CLEAN_SCHED = 3
OOC			= 4
BB			= 5

NO_CANCEL 	= 	True
REVERSE 	=	False



#===========================================
'''
  Base class for the room control system
	of lists and grids


stdDict[type] 	- ['display'] - Name
				- ['room']  - [number] 	-- ['marker'] 	- str
										-- ['style']	- str
										-- ['data'] 	- str

rvrsDict[number] - type

'''

#===========================================
class RGNew(object) :
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
		
		roomSet = set()

		for roomq in roomlist :
			roomSet.add(roomq.roominfo)

		#step through each occupied room, mark roominfolist
		for tnd in TypeNameDict :
			roominfo = RoomInfo.objects.filter(type=tnd).order_by("number")
			for ri in roominfo :
				if ri in roomSet :	
					ri.current = 1
				else: 
					ri.current = 0	
			displayRooms.append({
				'head' : TypeNameDict[tnd],
				'type' : tnd,
   			    'list': roominfo,
				 })
	
		# we have a set of occupied rooms	

		return displayRooms


















#===========================================
class RGBasic(object):

	type_list 	= SortOrderDict

	# gives me the type of room from room number
	rvrsDict = {}
	typeSubHeading = ""

	def __init__(self) :
		
		self.makeStdDict()

	#-------------------------------------------
	# we get a reservation and make our marks
	#-------------------------------------------
	def rsvn_select(self,rsvn):
	#-------------------------------------------
		self.start		= rsvn.dateIn.isoformat()
		self.end 		= rsvn.dateOut.isoformat()
		self.NO_CANCEL 	= True
		
		
		roomlst = []
		
		# find Yesterday checked out rooms Rooms
		for os in Room.objects.filter(rsvn__dateOut__exact = self.start).exclude( rsvn__status__exact = "cancel") :
			roomlst.append(os.roominfo.number)
		self.mark(roomlst,'last')
	
		# find rooms for rsvns
		self.select()
		self.mark(self.roomsFound,'rsvd')
		
		
		roomlst = []
		# find Yesterday checked out rooms Rooms
		# b2b date is checkout yesterday
		backDate = (rsvn.dateIn + timedelta(days=1)).isoformat()
		for os in self.roomListing.filter(rsvn__dateOut__exact = backDate) :
			roomlst.append(os.roominfo.number)
		self.mark(roomlst,'b2b')


		
		roomlst = []
		
		# find my rooms
		for rs in Room.objects.filter(rsvn__id__exact=rsvn.id) :
			roomlst.append(rs.roominfo.number)
		self.mark(roomlst,'mine')


		roomlst = []
		
		# find OOC Rooms
		for os in RoomInfo.objects.filter(current__exact=OOC) :
			roomlst.append(os.number)
		self.mark(roomlst,'ooc')

		
	
	#-------------------------------------------
	# select -- query object rsvnListing using
	#-------------------------------------------
	def select(self):
	#-------------------------------------------
		self.roomsFound = []
		rFound = []
		self.roomListing = Room.objects.filter(
			Q(rsvn__dateIn__gte = self.start,   rsvn__dateIn__lt= self.end  )   |
			Q(rsvn__dateOut__gt = self.start,  rsvn__dateOut__lte= self.end  )  |
			Q(rsvn__dateIn__lte = self.start,   rsvn__dateOut__gte= self.end  )
			)
			
		if self.NO_CANCEL :
			self.roomListing = self.roomListing.exclude(rsvn__status__exact='cancel')
		
		for rs in self.roomListing :
			rFound.append(rs.roominfo.number)
		self.roomsFound = set(rFound)

	#-------------------------------------------
	def mark(self,listing,mark) :
	# marker = "ooc" "rsvd" "mine" "b2b" "last"
	#-------------------------------------------
		for r in listing  :
			self.stdDict[self.rvrsDict[r]]['room'][r]['marker'] = mark
	
	#-------------------------------------------
	def makeStdDict(self) :
	#-------------------------------------------
		self.stdDict = {}
		for type in SortOrderDict :
			self.stdDict[type] = {}
			self.stdDict[type]['display'] = TypeNameDict[type]
			self.stdDict[type]['room'] = {}
			room = RoomInfo.objects.filter(type__exact=type)
			for r in room :
				
				# make tooltip here
				con = ""
				if r.connect > " ":
					con = "connect - {}".format(r.connect)
				tooltip = "{} bed - {} ".format(r.beds,con)
				
				# make rvrsDict here
				self.rvrsDict[r.number] = type
				self.stdDict[type]['room'][r.number] = {
					"marker" : "", "style" :"","data":tooltip }
	#-------------------------------------------
	def roomGrid(self):
	#-------------------------------------------
		code = []
		for heading in SortOrderDict :
			code.append("<tr><th>{}</th>".format(TypeNameDict[heading]))
			code.append("<td>{}</td>".format(self.typeSubHeading))
			code.append("<td>")
			for room in sorted(self.stdDict[heading]['room']) :
				marker = self.stdDict[heading]['room'][room]['marker']
				style  = self.stdDict[heading]['room'][room]['style']
				data  = self.stdDict[heading]['room'][room]['data']
				code.append("<button title='{3}' class='{0}' name='roomSelect'  style='{2}' value='{1}'>{1}</button>".format(marker,room,style,data))
			code.append("</td></tr>")
		return " ".join(code)
		
	#-------------------------------------------
	def room_ok(self,roomNumber):
	#-------------------------------------------
		mark = self.stdDict[self.rvrsDict[roomNumber]]['room'][roomNumber]['marker'] 
		answer = False
		if   mark == "" :
			answer = True
		if self.request.user.has_perm('rsvn.delete_rsvn') and mark in ['last', 'b2b', 'ooc'] :
			answer = True
		return answer
		
	#-------------------------------------------
	def change_room(self,roomNumber,value):
	#-------------------------------------------
		self.stdDict[self.rvrsDict[roomNumber]]['room'][roomNumber]['marker'] = value 

