from datetime import date
from rsvn.views import *
from django.views.generic import View

# Mango View class  -- The low level class viewmaker
# takes care of the arguments checking with arg_check(arg)
# and sends back all results. through self.results
# a really sweet class to build from
#
#=====================================================================
class MView(View) :
#=====================================================================
	form_class = ""
	template_name = ""
	result ={}
	request = ""
	args_put = {}
	args_get = {}

	# ---------------
	# We need event controls
	# ---------------
	def main (self) :
		pass
	# ---------------
	def post(self, request, *args, **kwargs) :
		self.args_put = request.POST
		self.request = request
		self.main()
		return render(request,self.template_name,self.result)
	# ---------------
	def arg_check(self,arg) :
		if arg in self.args_put :
			return True
		return False
	# ---------------
	def get(self, request, *args, **kwargs) :
		self.args_get = request.GET
		self.request = request
		self.main()
		return render(request,self.template_name,self.result )
		
#=====================================================================

def confirmation_gen (id) :
	today = date.today()
	fred  = "MNG-{:04}{:02}{:02}-{:04}".format(today.year,today.month,today.day,id)
	return fred
#=====================================================================
def roomGuide() :
	result = {}
	result['singleRoom'] = RoomInfo.objects.filter(beds=1)
	result['tripleRoom'] = RoomInfo.objects.filter(beds=3)
	result['connectRoom'] = RoomInfo.objects.exclude(connect="")
	return result


#=====================================================================
def rsvnListSelect(viewSelect)  :
	rlist =""

	if viewSelect == 'archive' :
		rlist = Rsvn.objects.all()
	elif viewSelect =='future' :
		rlist = Rsvn.objects.filter(dateOut__gte = date.today())
	elif viewSelect == '2week' :
		rlist = Rsvn.objects.filter(dateOut__gte = date.today(),dateIn__lte = date.today()+timedelta(days=14) )
	elif viewSelect == '1month' :
		rlist = Rsvn.objects.filter(dateOut__gte = date.today(),dateIn__lte = date.today()+timedelta(days=31) )
	elif viewSelect == 'cancel' :
		rlist = Rsvn.objects.filter(status__exact ='cancel')

	else :
		rlist = Rsvn.objects.filter(dateOut__gte = date.today(),dateIn__lte = date.today()+timedelta(days=14) )

	# take out cancelled reservations here
	if viewSelect in [ 'future','2week','1month' ] :
		rlist = rlist.exclude(status__exact = 'cancel')

	return rlist




#=====================================================================
class Req(object) :
#=====================================================================

	def __init__(self,request) :
		self.args = request.POST
		self.request = request
		self.result = {}
		
	def arg_check(self,arg) :
		if arg in self.args and self.args[arg] > "":
			return True
		return False
	# set the default value or pass value through
	def setDefault(self,arg,value) :
		self.result[arg] = value
		if self.arg_check(arg) :
			self.result[arg] = self.args[arg]
		return self.result[arg]

#=====================================================================
class RListing(Req) :
#=====================================================================
# this is the reservation list class
# We will need different listings throughout
# this class should aid in fast development
#=====================================================================
	query = ""
	result={}
	#-----------------------------------------------------
	def select(self)  :
	#------------------------------------------------------
		select = self.setDefault('viewSelect','2week')
			
		if 	select == 'archive' :
			rlist = Rsvn.objects.all()
		elif select =='future' :
			rlist = Rsvn.objects.filter(dateOut__gte = date.today())
		elif select == '2week' :
			rlist = Rsvn.objects.filter(dateOut__gte = date.today(),dateIn__lte = date.today()+timedelta(days=14) )
		elif select == '1month' :
			rlist = Rsvn.objects.filter(dateOut__gte = date.today(),dateIn__lte = date.today()+timedelta(days=31) )
		elif select == 'cancel' :
			rlist = Rsvn.objects.filter(status__exact ='cancel')
		else :
			rlist = Rsvn.objects.filter( dateOut__gte = date.today() )
		# take out cancelled reservations here
		if select in [ 'future','2week','1month' ] :
			rlist = rlist.exclude(status__exact = 'cancel')
		self.rlist = rlist

	#------------------------------------------------------
	def checked(self) :
	#------------------------------------------------------
		self.rlist = Rsvn.objects.filter( dateOut__gte = date.today(),status__exact = "checkin")
		self.query()
		self.listAddons()
		self.result.update({'rlist':self.rlist})	
	#------------------------------------------------------
	def reserved(self) :
	#------------------------------------------------------
		self.rlist = Rsvn.objects.filter( dateIn__gte = date.today()
						).exclude(status__exact = 'cancel'
						).exclude(status__exact = 'checkin')
		self.query()
		self.listAddons()
		self.result.update({'rsvn_list':self.rlist})	
	#------------------------------------------------------
	def make(self) :
	#------------------------------------------------------
		# this loads rlist with the selected  
		self.select()
		self.query()
		self.listAddons()
		# all the addon information
		return result

	#------------------------------------------------------
	def query(self) :
	#------------------------------------------------------
		# if we request a search
		if self.arg_check('query') :
			query = self.args['query']
			self.rlist = self.rlist.filter(
				Q(lastname__icontains = query) |
				Q(firstname__icontains = query) |
				Q(notes__icontains = query) |
				Q(confirm__icontains = query ) )
			self.result['query'] = query

	#------------------------------------------------------
	def listAddons(self) :
	#------------------------------------------------------
		for rv in self.rlist :
			roomck = Room.objects.filter(rsvn_id__exact = rv.id)
			tourck = Tour.objects.filter(rsvn_id__exact = rv.id)
			rv.assigned = len(roomck)
			rv.gridColor = getGridColor(rv.id)
			if tourck :
				rv.tourinfo = tourck[0]
			# if we haven't assigned all the rooms Indicate by color change
			if rv.assigned < rv.rooms :
				rv.textColor = 'brown'
			else :
				rv.textColor = 'black'
			# mark the cancels
			if rv.status == 'cancel' :
				rv.textStyle = "text-decoration:line-through;"

			rv.roomsSelected = roomck

#=====================================================================
def rsvnListMake(request) :
	result = {}
	viewSelect = '2week'

	if 'viewSelect' in request.POST :
		viewSelect = request.POST['viewSelect']
	result['viewSelect'] = viewSelect

	# if we request a search
	if 'query' in request.POST and request.POST['query'] > "" :
		query = request.POST['query']
		rvn_list = Rsvn.objects.all()
		rvn_list = rvn_list.filter(
			Q(lastname__icontains = query) |
			Q(firstname__icontains = query) |
			Q(notes__icontains = query))
		result['query'] = query
	# if not we do our filtered list
	else :
		rvn_list = rsvnListSelect(viewSelect)

	# here is all the addon information

	for rv in rvn_list :
		roomck = Room.objects.filter(rsvn_id__exact = rv.id)
		tourck = Tour.objects.filter(rsvn_id__exact = rv.id)
		rv.assigned = len(roomck)
		rv.gridColor = getGridColor(rv.id)
		if tourck :
			rv.tourinfo = tourck[0]
		# if we haven't assigned all the rooms Indicate by color change
		if rv.assigned < rv.rooms :
			rv.textColor = 'brown'
		else :
			rv.textColor = 'black'
		# mark the cancels
		if rv.status == 'cancel' :
			rv.textStyle = "text-decoration:line-through;"

		rv.roomsSelected = roomck
	result['rsvn_list'] = rvn_list
	return result
#=====================================================================
def roomListMake (rsvnid) :
	result = {}
	roomList = Room.objects.filter(rsvn_id__exact=rsvnid)
	result['assignedRooms'] = len(roomList)
	result['roomList'] = roomList
	return result
# ==================================================
# This is to keep the tabs in place after selected
# ==================================================
def tab_state(request) :
	result = {}
	result["mode"] = 0
	result["mode2"] = 0

	if 'mode' in request.POST :
		result['mode'] = request.POST['mode']
	if 'mode2' in request.POST :
		result['mode2'] = request.POST['mode2']

	return result

