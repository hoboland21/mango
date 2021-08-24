
from datetime import time, date, datetime, timedelta
from rsvn.models import *
from .roomStats import *

#--------------------------
def date_mark_text(srcdate) :
#--------------------------

	# This gives us the delta days in text
	dday = (date.today() - srcdate).days
	if dday == 1 :
		dd = " Yesterday"
	elif dday == -1 :
		dd = " Tomorrow"
	elif dday == 0 :
		dd = " Today"
	elif dday < 0 :
		dd = " %s days from now" % abs(dday)
	else :
		dd = " %s days ago" % abs(dday)

	return  dd

#--------------------------
def calendar_ops(request) :
#--------------------------
	result = {}
	caldate = datetime.strptime(request.session["dateSelect"],"%Y-%m-%d").date()
	

	if "dateSelect" in request.POST :
		pass
	
	if "datePlus" in request.POST :
		caldate = (caldate + timedelta(days=1))
	

	if "dateMinus" in request.POST :
		caldate =  (caldate - timedelta(days=1))

	if "dateGo" in request.POST :
		request.session["dateSelect"] = request.POST["dateGo"] 
		request.session["panel"] = "calendarcard" 

	request.session["dateSelect"] = datetime.strftime(caldate,"%Y-%m-%d") 
	return date_mark_text(caldate)


#--------------------------
class CalClass(object) :
#--------------------------
	def __init__(self,request) :
		self.currdate = datetime.strptime(request.session["dateSelect"],"%Y-%m-%d").date()
		self.currHouseRsvn = self.rsvnList(self.currHouse())
		self.currCheckinRsvn = self.rsvnList(self.currCheckin())
		self.currCheckoutRsvn = self.rsvnList(self.currCheckout())

	def currCheckin(self) :
		return Room.objects.filter(rsvn__dateIn=self.currdate).order_by("roominfo__number")

	def currCheckout(self) :
		return Room.objects.filter(rsvn__dateOut=self.currdate).order_by("roominfo__number")

	def currHouse(self) :
		rmlist = rooms_in_span(self.currdate,self.currdate)
		return  rmlist.exclude(rsvn__dateIn=self.currdate).exclude(rsvn__dateOut=self.currdate)

	def rsvnList(self,roomlist) :
		res = {}
		for rl in roomlist :
			try:
				res[rl.rsvn.id].append(rl)
			except:
				res[rl.rsvn.id] = []
				res[rl.rsvn.id].append(rl)

		return res


	def calMapper(self) :
		calmap = RoomMapper()
		calmap.build_tree()
		calmap.room_marker(self.currHouse(),"inhouse")
		calmap.room_marker(self.currCheckin(),"checkin")
		calmap.room_marker(self.currCheckout(),"checkout")

		return calmap.room_map


