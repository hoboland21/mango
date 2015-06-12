from rsvn.tools.misc import *
from rsvn.models import *
from django.shortcuts import redirect
from rsvn.vctools.roomGrid import *
#from rsvn.vc import event,calendar,agent,chat
from django.utils.decorators import method_decorator
from rsvn.vc.vclass import VClass
from rsvn.vctools.tools import *
from rsvn.vctools.packing import *
#from rsvn.vctools.tools import *

#================================================================================================
class RsvnCreate (VClass) :
#================================================================================================
	template_name = "revise/detailForm.html"
	result ={}
	request = ""
	args_put = {}
	args_get = {}
	# ==========================================================	
	@method_decorator(login_required)

	def post(self, request, *args, **kwargs) :
		self.rsvnid = 0
		self.args_put = request.POST
		self.request = request
		self.main()
		if self.rsvnid :
			return redirect ('rsvnupdate',self.rsvnid)
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )

	# ==========================================================
	def loadBlankForm(self) :
		self.result['RsvnForm'] = RsvnForm()
		self.result['ServiceForm']= ServiceForm()
		self.result['SchemeForm'] = SchemeForm()
		self.result['TourForm'] = TourForm()
		self.result['EventForm'] = EventForm()

	# ==========================================================
	def loadEditForm(self) :
		rsvnForm = RsvnForm(self.args_put)
		if rsvnForm.is_valid() :
			rsvn = rsvnForm.save(commit=False) 
			rsvn.save()
			rsvn.clerk = self.request.user.username
			rsvn.confirm = confirm_gen(rsvn.id)
			self.rsvnid = int(rsvn.id)
			rsvn.save()			
			
			serviceForm = ServiceForm(self.args_put)
			if serviceForm.is_valid() : 
				service = serviceForm.save(commit=False) 
				if len(serviceSplitter(service)) :
					service.rsvn = rsvn
					service.save() 
			
			schemeForm = SchemeForm(self.args_put)
			if schemeForm.is_valid() : 
				scheme = schemeForm.save(commit=False) 
				scheme.rsvn = rsvn
				scheme.save() 
			
			tourForm = TourForm(self.args_put)
			if tourForm.is_valid() : 
				tour = tourForm.save(commit=False) 
				tour.rsvn = rsvn
				tour.save()

			eventForm = EventForm(self.args_put)
			if eventForm.is_valid() : 
				event = eventForm.save(commit=False) 
				event.rsvn = rsvn
				event.save()


		else :
			self.result['RsvnForm'] = RsvnForm(self.args_put)
			self.result['ServiceForm']  = ServiceForm(self.args_put)
			self.result['SchemeForm'] = SchemeForm(self.args_put)
			self.result['TourForm'] = TourForm(self.args_put)
			self.result['EventForm'] = EventForm(self.args_put)

	# ==========================================================
	def main(self) :
		self.result["RC1List"] = RC1List
		self.result["RC2List"] = RC2List
		self.result["create"] = True
		if self.arg_check('saveForm') :
			self.loadEditForm()
		else:	 
			self.loadBlankForm()
#================================================================================================
class RsvnUpdate (VClass) :
#================================================================================================
	template_name = "revise/detailForm.html"
	result ={}
	request = ""
	args_put = {}
	args_get = {}

	#----------------------------------
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs) :
	#----------------------------------
		self.args_put = request.POST
		self.request = request
		self.main()
		if self.rsvnid == 0 :
			return redirect ('rsvnlist',0)
		if self.rsvnid != self.rsvn.id :
			return redirect ('rsvnupdate',self.rsvnid)
				
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )

	#----------------------------------
	def main(self) :
	#----------------------------------
		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid
		self.result["RC1List"] = RC1List
		self.result["RC2List"] = RC2List
		

		# Save form 
		if self.arg_check('saveForm') :
			self.loadEditForm()
		else :	
			self.getDBObj()
			self.loadObjForm()


				
		# start our Room grid build here
		rs1 = RGBasic()
		rs1.request = self.request
		rs1.rsvn_select(self.rsvn)


		# adding a room is selected
		if self.arg_check("roomSelect") :
			roomNumber = self.args_put['roomSelect']
			if rs1.room_ok(roomNumber) and len(Room.objects.filter(rsvn__id__exact=self.rsvnid)) < self.rsvn.rooms:
				roominfo = RoomInfo.objects.get(number__exact = roomNumber)
				room  = Room(rsvn=self.rsvn,roominfo=roominfo,roomstatus='none')
				room.save()
				rs1.change_room(roomNumber,"mine")

		# deleting a room is selected
		if self.arg_check("delRoom") :
			roomNumber = self.args_put['delRoom']
			rs1.change_room(roomNumber,"")
			rmchk =	Room.objects.get(roominfo__number = roomNumber,rsvn_id = self.rsvn.id)
			rmchk.delete()




		# adding a blog entry
		if self.arg_check("saveBlog") :
			blogForm = RsvnBlogForm(self.args_put)
			if blogForm.is_valid() : 
				blog = blogForm.save(commit=False)
				blog.clerk =  self.request.user.username
				blog.rsvn = self.rsvn

				blog.save()

		# make a list of the blogs
		self.result["blogList"] = RsvnBlog.objects.filter(rsvn_id__exact=self.rsvn.id).order_by('-time')

		# check my toggle board
		self.roomToggles()

		#==========================
		# rebuild the page with new data
		self.rsvn.assigned = len(self.rsvn.room_set.all()) 
		self.rsvn.roomset = self.rsvn.room_set.all()
		self.result["rsvnRec"] = self.rsvn 	

		# we have a basic room grid
		self.result['roomgrid'] = rs1.roomGrid()

		#==========================
		# if we receive a delete record delete and go to 0
		# this is from dialog
		if self.arg_check('deleteVerify') : 
			if self.args_put['deleteVerify'] == 'yes' :
				self.rsvn.delete()
				self.rsvnid = 0
	
		#==========================
		# if we receive a duplicate record command
		# this is from dialog
		if self.arg_check('cloneVerify') : 
			if self.args_put['cloneVerify'] == 'yes' :
				self.duplicateForm()
			# clone a record here			
	
	
	
	
	
	#----------------------------------
	def roomToggles(self) :
	#----------------------------------
		#pressing roomInStatus 
		if self.arg_check("roomInSelect") :
			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomInSelect"])
			room.roomstatus = "checkin"
			room.save()
		#pressing roomOutStatus 
		if self.arg_check("roomOutSelect") :
			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomOutSelect"])
			room.roomstatus = "checkout"
			room.save()

		#pressing roomNoneStatus 
		if self.arg_check("roomNoneSelect") :
			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomNoneSelect"])
			room.roomstatus = "none"
			room.save()
		#==========================
		# we check for a global button push
		check = ""
		#pressing globalIn 
		if self.arg_check("globalIn") :
			check ="checkin" 
		#pressing globalOut 
		if self.arg_check("globalOut") :
			check="checkout"
		#pressing globalNone 
		if self.arg_check("globalNone") :
			check="none"

		if check != "" :
			for room in Room.objects.filter(rsvn__id=self.rsvnid) :
				room.roomstatus = check
				room.save()
	#----------------------------------
	def getDBObj(self) :
	#----------------------------------
		self.rsvn = Rsvn.objects.get(id=self.rsvnid)
		self.service = Service()
		self.scheme = Scheme()
		self.tour = Tour()
		self.event = Event()
		
		if Tour.objects.filter(rsvn__id=self.rsvnid) :
			self.tour = Tour.objects.get(rsvn__id=self.rsvnid)
		if Service.objects.filter(rsvn__id=self.rsvnid) :
			self.service = Service.objects.get(rsvn__id=self.rsvnid)
		if Scheme.objects.filter(rsvn__id=self.rsvnid) :
			self.scheme = Scheme.objects.get(rsvn__id=self.rsvnid)
		if Event.objects.filter(rsvn__id=self.rsvnid) :
			self.event = Event.objects.get(rsvn__id=self.rsvnid)


	#----------------------------------
	def duplicateForm(self) :
	#----------------------------------
		rsvnForm = RsvnForm(self.args_put)

		if rsvnForm.is_valid() :
			rsvn = rsvnForm.save(commit=False)
			rsvn.save()	

			rsvn.clerk = self.request.user.username
			rsvn.confirm = confirm_gen(rsvn.id)
			self.rsvnid = int(rsvn.id)
			rsvn.save()	

			tourForm = TourForm(self.args_put)
			if tourForm.is_valid() : 
				tour = tourForm.save(commit=False) 
				tour.rsvn = rsvn
				tour.save()

			schemeForm = SchemeForm(self.args_put)
			if schemeForm.is_valid() : 
				scheme = schemeForm.save(commit=False) 
				scheme.rsvn = rsvn
				scheme.save() 
	
	

	#----------------------------------
	def loadEditForm(self) :
	#----------------------------------

		self.getDBObj()
		self.result['RsvnForm'] 	= RsvnForm(self.args_put)
		self.result['ServiceForm']  = ServiceForm(self.args_put)
		self.result['SchemeForm'] 	= SchemeForm(self.args_put)
		self.result['TourForm'] 	= TourForm(self.args_put)			
		self.result['EventForm'] 	= EventForm(self.args_put)			

		self.rsvn = Rsvn.objects.get(pk=self.rsvnid)
		rsvnForm = RsvnForm(self.args_put,instance=self.rsvn)
		if rsvnForm.is_valid() :
			self.rsvn = rsvnForm.save(commit=False)
			self.rsvn.save()	
			
			serviceForm = ServiceForm(self.args_put,instance=self.service)
			if serviceForm.is_valid() : 
				service = serviceForm.save(commit=False) 
				service.rsvn = self.rsvn
				service.save() 
			
			schemeForm = SchemeForm(self.args_put,instance=self.scheme)
			if schemeForm.is_valid() : 
				scheme = schemeForm.save(commit=False) 
				scheme.rsvn = self.rsvn
				scheme.save() 
			
			tourForm = TourForm(self.args_put,instance=self.tour)
			if tourForm.is_valid() : 
				tour = tourForm.save(commit=False) 
				tour.rsvn = self.rsvn
				tour.save()

			eventForm = EventForm(self.args_put,instance=self.event)
			if eventForm.is_valid() : 
				event = eventForm.save(commit=False) 
				event.rsvn = self.rsvn
				event.save()


	#----------------------------------
	def loadObjForm(self) :
	#----------------------------------
		self.result['RsvnForm'] = RsvnForm(instance=self.rsvn)
		self.result['ServiceForm']= ServiceForm(instance=self.service)
		self.result['SchemeForm'] = SchemeForm(instance=self.scheme)
		self.result['TourForm'] = TourForm(instance=self.tour)
		self.result['EventForm'] = EventForm(instance=self.event)
		self.result['RsvnBlogForm'] = RsvnBlogForm()






