#from rsvn.tools.misc import *
from django.db.models import Q
from rsvn.models import *
#from django.shortcuts import redirect
#from rsvn.vctools.roomGrid import *
#from rsvn.vc import event,calendar,agent,chat
#from django.views.generic.base import View
#from django.utils.decorators import method_decorator
from decimal import *
from rsvn.vc.current import OOC
#-------------------------------------------------------

#-------------------------------------------
def  availRooms(dateFrom,dateTo) :
#-------------------------------------------
	avail_dict = {}
	for RTC in ROOM_TYPE_CHOICES :
		avail_dict[RTC[0]] = 0
	
	rooms = Room.objects.filter(
		Q(rsvn__dateIn__gte = dateFrom,  rsvn__dateIn__lt= dateTo  )   |
		Q(rsvn__dateOut__gt = dateFrom,  rsvn__dateOut__lte= dateTo  )  |
		Q(rsvn__dateIn__lte = dateFrom,  rsvn__dateOut__gte= dateTo  )
		).exclude(rsvn__status__exact='cancel')

	rooms_selects = []

	for room in rooms :
		rooms_selects.append(room.roominfo.number)

	rooms_selects = set(rooms_selects)
	
	allRooms = RoomInfo.objects.all().exclude(current__exact=OOC)
	
	for rm in rooms_selects:
		allRooms = allRooms.exclude(number__exact=rm)
	
	for rm in allRooms:
		avail_dict[rm.type] += 1
		
	return avail_dict

#-------------------------------------------
def seasonCheck(dateFrom,dateTo):
# we grab the applicable season(s) for this rsvn.. we make a list called self.season
#-------------------------------------------
	season = Season.objects.filter(
		Q(beginDate__gte = dateFrom, beginDate__lte = dateTo) |
		Q(beginDate__lte = dateFrom, endDate__gte = dateFrom) |
		Q(beginDate__lt = dateTo, endDate__gte = dateTo)
		)
	
	for seas in season :
		firstday = max(seas.beginDate,dateFrom)
		lastday = min(seas.endDate, dateTo)
		
		seas.days = (lastday - firstday).days+1
		if lastday == dateTo :
			seas.days += -1


	return season



#-------------------------------------------------------
def moneyfmt(value, places=2, curr='$', sep=',', dp='.', pos='', neg='-', trailneg='') :
#-------------------------------------------------------
 
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))



