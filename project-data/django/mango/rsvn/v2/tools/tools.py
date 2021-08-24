#from rsvn.tools.misc import *
from django.db.models import Q
from rsvn.models import *
from decimal import *
from rsvn.lists import *

import logging
#Create and configure logger 
logging.basicConfig(filename="rsvn10.log", 
                    format='%(asctime)s:%(name)s:%(message)s', 
                    filemode='w',level=logging.DEBUG) 

#import logging
#logger=logging.getLogger(__name__) 

#-------------------------------------------------------
def rsvns_in_span(dateStart,dateEnd,cancel):
#------------------------------------------
	rsvn_list = Rsvn.objects.filter(
		Q(dateIn__gte = dateStart,   dateIn__lte= dateEnd  )   |
		Q(dateOut__gt = dateStart,  dateOut__lt=dateEnd  )  |
		Q(dateIn__lte = dateStart,   dateOut__gte=dateEnd  )
		)
	if cancel :
		rsvn_list.exclude(status__exact='cancel') 

	for rsvn in rsvn_list :
		rsvn.roomset = rsvn.room_set.all()
		if rsvn.scheme_set.all() :
			rsvn.scheme = rsvn.scheme_set.all()[0]

	return rsvn_list

#-------------------------------------------
def  rooms_in_span(dateStart,dateEnd) :
#-------------------------------------------
	room_list = Room.objects.filter(
		Q(rsvn__dateIn__gte = dateStart,  rsvn__dateIn__lt= dateEnd  )   |
		Q(rsvn__dateOut__gt = dateStart,  rsvn__dateOut__lte= dateEnd  )  |
		Q(rsvn__dateIn__lte = dateStart,  rsvn__dateOut__gte= dateEnd )
		)
	return room_list

