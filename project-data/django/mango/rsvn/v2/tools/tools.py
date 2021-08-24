#from rsvn.tools.misc import *
from django.db.models import Q
from rsvn.models import *
from decimal import *
from rsvn.lists import *
#-------------------------------------------------------






#-------------------------------------------
# bring in a Room query and make it display ready seperated by type
#-------------------------------------------
class RoomInfoDisplayCtrl(object) :
#-------------------------------------------

	#----------------
	def __init__(self) :
	#----------------
		self.displayArray =  []
		for sol in SORT_ORDER_LIST :
			roominfo = RoomInfo.objects.filter(type=sol).order_by("number")
			self.displayArray.append({
				'head' : TYPE_NAME_DICT[sol],
				'type' : sol,
				'list': roominfo,
				 })
	#----------------
	def listing(self) :
	#----------------
		return self.displayArray

#-------------------------------------------
def rsvn_select(dateStart,dateEnd,cancel):
#-------------------------------------------
	rList = Rsvn.objects.filter(
		Q(dateIn__gte = dateStart,   dateIn__lte= dateEnd  )   |
		Q(dateOut__gt = dateStart,  dateOut__lt=dateEnd  )  |
		Q(dateIn__lte = dateStart,   dateOut__gte=dateEnd  )
		)
	if cancel :
		rList.exclude(status__exact='cancel') 


	for rsvn in rList :
			rsvn.roomset = rsvn.room_set.all()
			if rsvn.scheme_set.all() :
				rsvn.scheme = rsvn.scheme_set.all()[0]

	return rList

#-------------------------------------------
def  availRooms(dateFrom,dateTo) :
#-------------------------------------------

	rooms = Room.objects.filter(
		Q(rsvn__dateIn__gte = dateFrom,  rsvn__dateIn__lt= dateTo  )   |
		Q(rsvn__dateOut__gt = dateFrom,  rsvn__dateOut__lte= dateTo  )  |
		Q(rsvn__dateIn__lte = dateFrom,  rsvn__dateOut__gte= dateTo  )
		).exclude(rsvn__status__exact='cancel')

	allRooms = RoomInfo.objects.all().exclude(current__exact=OOC)
