from django.db.models import Q
from rsvn.models import *



#-------------------------------------------------------
def confirm_gen (id) :
#-------------------------------------------------------
	today = date.today()
	return 'MNG-{:04}{:02}{:02}-{:04}'.format(today.year,today.month,today.day,id)

#-------------------------------------------------------
def serviceSplitter(service) :
#-------------------------------------------------------
	names = service._meta.get_fields()
	servlist =[]	
	for field in names :
		value = getattr(service,field.name,None)
		if value == True  and field.name in SERVICE_FIELDS:
			
			servlist.append([field.name, SERVICE_FIELDS[field.name],SERVICE_FIELDS_ABV[field.name] ])
	return servlist		

#-------------------------------------------------------
def rsvnPacker(rsvn) :
#-------------------------------------------------------
	rsvn.roomset = rsvn.room_set.all().order_by('roominfo__number')
	rsvn.assigned = len(rsvn.roomset)
	rsvn.unassigned = rsvn.rooms - rsvn.assigned

	rsvn.blogset = rsvn.rsvnblog_set.all().order_by('time')
	tourset = rsvn.tour_set.all()		
	if tourset :
		rsvn.tourset = tourset[0]
	
	serviceset = rsvn.service_set.all()
	if serviceset :
		rsvn.serviceset  = serviceSplitter(serviceset[0]) 
		rsvn.serviceList = []
		for rs in rsvn.serviceset :
			rsvn.serviceList.append(rs[1])



	rsvn.gridColor = 'white'
	if rsvn.scheme_set.all() :
		scheme = rsvn.scheme_set.all() 
		rsvn.gridColor = scheme[0].gridColor
		rsvn.schemeset = scheme[0]
	



	# if we haven't assigned all the rooms Indicate by color change
	
	if rsvn.assigned < rsvn.rooms :
		rsvn.textColor = 'brown'
	else :
		rsvn.textColor = 'black'

	# mark the cancels
	
	if rsvn.status == 'cancel' :
		rsvn.textStyle = "text-decoration:line-through"
	return rsvn

#-------------------------------------------------------
def rsvnidPacker(rsvnid) :
#-------------------------------------------------------
	rsvn = Rsvn.objects.get(pk=rsvnid)
	return rsvnPacker(rsvn)
