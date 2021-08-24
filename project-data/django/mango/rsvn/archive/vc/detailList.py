from rsvn.models import *
from django.shortcuts import redirect
from rsvn.tools.misc import *
from rsvn.vctools.packing import *
from django.utils.decorators import method_decorator
from rsvn.views import *
from datetime import time, date
from django.utils import timezone
import pytz
from rsvn.vc.vclass import VClass

SERVICE_FIELDS = { 
		'from_airport'	: 'From Airport Trans',
		'to_airport'	: 'To Airport Trans',
		'breakfast'		: 'Breakfast',
		'earlyin'		: 'Early Check In',
		'lateout' 		: 'Late Check Out',
		'connect' 		: 'Connecting Room',
		'dailymaid'		: 'Daily Maid Service',
		'extrabed'		: 'Extra Bed',
		'mango' 		: 'Mango Access',
		'crib'			: 'Baby Crib'}


#=====================================================================
class RListingNew(object) :
#=====================================================================
# this is the reservation list class
#		self.args = { 
#		"listSort" 	: "dateIn",
#		"listSelect" 	: "inHouse",
#		"agentSelect" 	: "FIT",
#		"dateSelect"	:  date.today().isoformat(),

	result={}
	#------------------------------------------------------
	def __init__(self,args) :
	#------------------------------------------------------
		self.workrlist = Rsvn.objects.all()
		self.agentList = Agent.objects.all()
		self.args = args
		self.rlist = {}
		
		self.filter()
	#------------------------------------------------------
	def filter(self) :
	#------------------------------------------------------
		self.filterLabel = "--"
		if self.args['listSelect'] == 'cancel' :
			self.filterLabel = "Cancelled Reservations"
			self.rlist =self.workrlist.filter( status__exact = 'cancel')
			
		elif self.args['listSelect'] == 'current' :
			self.filterLabel = "Current Active Reservations"
			self.rlist =self.workrlist.filter(dateOut__gte = date.today()).exclude(status__exact = 'cancel')		

		elif self.args['listSelect'] == 'checkin' :
			self.filterLabel = "Check In Today"
			self.rlist =self.workrlist.filter(dateIn__exact = date.today()).exclude(status__exact = 'cancel')
			
		elif self.args['listSelect'] == 'checkout' :
			self.filterLabel = "Check Out Today"
			self.rlist =self.workrlist.filter( dateOut__exact = date.today()).exclude(status__exact = 'cancel')
		
		elif self.args['listSelect'] == 'inHouse' :
			self.filterLabel = "In House Rooms Occupied"
			self.rlist =self.workrlist.filter(dateOut__gte = date.today(),dateIn__lte = date.today()).exclude(status__exact = 'cancel')

		elif self.args['listSelect'] == 'reserved' :
			self.filterLabel = "Current Reservations"
			self.rlist =self.workrlist.filter( dateIn__gte = date.today()
						).exclude(status__exact = 'cancel'
						).exclude(status__exact = 'checkin')
						
		elif self.args['listSelect'] == 'agent' : 
			self.filterLabel = "Agent : " + self.args['agentSelect'] 
			self.rlist = self.workrlist.filter(tour__agent__agency__exact = self.args['agentSelect'])
			
				
			
		elif self.args['listSelect'] == 'archive' and self.args['query'] > "":
			self.filterLabel = "Archive Search"
			self.rlist =self.workrlist

		self.do_query()
	#------------------------------------------------------
	def do_query(self) :
	#------------------------------------------------------
		# if we request a search
		query = self.args["query"]
		if self.rlist :
			self.rlist = self.rlist.filter(
				Q(lastname__icontains = query) |
				Q(firstname__icontains = query) |
				Q(notes__icontains = query) |
				Q(confirm__icontains = query )  |
				Q(tour__agent__agency__icontains = query) 
				)
		self.sortlist()
		
	#------------------------------------------------------
	def sortlist(self) :
	#------------------------------------------------------
		if self.rlist :
			if self.args['listSort'] in ('lastname','firstname','dateIn', 'dateOut') :
				self.rlist = self.rlist.order_by(self.args['listSort'])
	
	
		self.listComplete()
		
	#------------------------------------------------------
	def listComplete(self) :
	#------------------------------------------------------
		for rv in self.rlist :
			rv = rsvnPacker(rv)				

			rv.highlight = '0'
			rv.warning = '0'
			

	#------------------------------------------------------
	def listHighlight(self,rsvnid) :
	#------------------------------------------------------
		for rv in self.rlist :
			if rv.id == rsvnid :
				rv.highlight = '1'
			
	#------------------------------------------------------
	def checkWarning(self) :
	#------------------------------------------------------
		oocList = Rsvn.objects.filter(room__roominfo__current__exact=OOC, dateIn__gte=datetime.today())
		hitList = []
		for hit in oocList :
			hitList.append(hit.id)	
		for rv in self.rlist :
			if rv.id in hitList :
				rv.highlight = '2'

#=====================================================================
class RsvnList (VClass)	 :
#=====================================================================

	form_class = ""
	template_name = "revise/detailList.html"
	result ={}
	request = ""
	args_put = {}
	args_get = {}

	# ---------------
	# We need event controls
	# ---------------

	#-------------------------------------------------------
	def args_fix (self) :
	#-------------------------------------------------------
		# our session args
		self.args = { 
		"listSort" 	: "dateIn",
		"listSelect" 	: "inHouse",
		"agentSelect" 	: "FIT",
		"dateSelect"	:  date.today().isoformat(),

		}
		for arg in self.args :
			# if we bring them in
			if self.arg_check(arg) :
				self.args[arg] = self.args_put[arg]
			# if we pull from session	
			elif  arg in self.request.session  :
				self.args[arg] = self.request.session[arg]
			#save these arguments back to session
			self.request.session[arg] = self.args[arg]
			# send arguments back to context

		self.args.update({"query":""})
		if self.arg_check('query') :
			self.args['query'] = self.args_put['query']
			

	#-------------------------------------------------------
	def main (self) :
	#-------------------------------------------------------
		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid
		# Header Web List
		
		self.result["webCount"] = len(WebRsvn.objects.all().exclude(rsvn__gt=0))
		# lets check list arguments
		# arrange our list search boxes and pull in cookie data
		self.args_fix()
		
		self.displayRList()
	
		# send arguments back to HTML page
		self.args_send()
		
		# load a reservation to view in list header 
		if self.rsvnid > 0 :
			self.result['rsvnRec'] = rsvnidPacker(self.rsvnid)
#		self.result.update (csrf(self.request))
	
	#-------------------------------------------------------
	def displayRList(self) :
	#-------------------------------------------------------
		# build a new list class object
		newList = RListingNew(self.args)
		
		self.result['filterLabel']  = newList.filterLabel
		newList.listHighlight(self.rsvnid)
		newList.checkWarning()
		self.result['rlist'] = newList.rlist
		self.result["agentList"] = Agent.objects.all()


	
