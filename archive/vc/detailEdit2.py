from rsvn.tools.misc import *
from rsvn.models import *
from rsvn.forms import *

from django.db.models import Q

from django.shortcuts import redirect
from rsvn.vctools.roomGrid import *
#from rsvn.vc import event,calendar,agent,chat
from django.utils.decorators import method_decorator
from rsvn.vc.vclass import *
from rsvn.vctools.tools import *
from rsvn.vctools.packing import *
#from rsvn.vctools.tools import *

#================================================================================================
class RsvnMain(SmallVClass) :
#================================================================================================
	template_name = "revise/detailForm2.html"

# ==========================================================
	#------------------
	def main(self) :
	#------------------
		if "newrsvn" in self.request.POST :
			self.rsvnid = 0
			self.request.session["rsvnid"] = 0
			self.request.session["panel"] = "rsvncard"			

		if "rsvnid" not in self.request.session:
			self.request.session["rsvnid"] = 0
		if "panel" not in self.request.session:
			self.request.session["panel"] = "welcomecard"			
		self.creator()
		self.updater()
		self.rsvn = Rsvn()
		self.init()
		self.load_rsvn()
		self.panel()

		if "query" in self.request.POST and len(self.request.POST['query']):
			self.search_query()
		if "dquery" in self.request.POST and len(self.request.POST['dquery']):
			self.search_query()

# ==========================================================
	#------------------
	def search_query(self) :
	#------------------
		if "query" in self.request.POST and len(self.request.POST['query']):
			self.result["query"] = self.request.POST["query"]
			self.result["dquery"] = ""

			q = self.request.POST["query"]
			qlist = Rsvn.objects.filter(Q(lastname__icontains=q)|Q(firstname__icontains=q)
				).order_by('-dateIn')

			if not "include_cancel" in self.request.POST :
				qlist = qlist.exclude(status="cancel") 

			self.result["qlist"] = qlist	

		elif "dquery" in self.request.POST and len(self.request.POST['dquery']):
			dq = self.request.POST["dquery"]
			self.result["dquery"] = dq
			self.result["query"] = ''
			dqlist = Rsvn.objects.filter(dateIn__lte = dq,dateOut__gte=dq).order_by('-dateIn')

			if not "include_cancel" in self.request.POST :
				dqlist = dqlist.exclude(status="cancel") 

			self.result["qlist"] = dqlist	
		else:
			self.result["qlist"] =''


# ==========================================================
	#------------------
	def creator(self) :
	#------------------
		if "delete-rsvn" in self.request.POST and self.request.session["rsvnid"] :
			Rsvn.objects.get(id=self.request.session["rsvnid"]).delete()

		if "create-rsvn" in self.request.POST and not self.request.session["rsvnid"] :
			rsvnForm = RsvnForm(self.request.POST)
			if rsvnForm.is_valid() :
				rsvn = rsvnForm.save(commit=False) 
				rsvn.save()
				rsvn.clerk = self.request.user.username
				rsvn.confirm = confirm_gen(rsvn.id)
				rsvn.save()			
				self.request.session["rsvnid"] = int(rsvn.id)
				self.rsvn=rsvn
				scheme = Scheme(rsvn=self.rsvn)
				scheme.save()


	#------------------
	def updater(self) :
	#------------------
		if self.request.session["rsvnid"] :
			try: 
				self.rsvn = Rsvn.objects.get(id=self.request.session["rsvnid"])

				if "update-scheme" in self.request.POST :
					try:
						scheme = Scheme.objects.get(rsvn=self.rsvn)
						schemeForm = SchemeForm(self.request.POST,instance=scheme)
						if schemeForm.is_valid() : 
							scheme = schemeForm.save() 
					except:
						pass
				if "update-rsvn" in self.request.POST :
					try:
						rsvnForm = RsvnForm(self.request.POST,instance=self.rsvn)
						if rsvnForm.is_valid() : 
							self.rsvn  = rsvnForm.save() 
					except:
						pass

				if "save-blog" in self.request.POST  :
					rsvnBlog = RsvnBlog(rsvn=self.rsvn,clerk=self.request.user)
					rsvnBlogForm =  RsvnBlogForm(self.request.POST,instance=rsvnBlog) 
					if rsvnBlogForm.is_valid() : 
						rsvnBlogForm.save() 
				
				if "room-select" in self.request.POST :
		### Here is a sequence problem
					rg1 = RGNew(self.request)
		###################################			
					if  len(rg1.rsvn_rooms) < self.rsvn.rooms :
						roomsel = self.request.POST["room-select"]
						ri = RoomInfo.objects.get(id=roomsel)
						room = Room(roominfo=ri,rsvn=self.rsvn,roomstatus="select")
						room.save()
				if "room-delete" in self.request.POST :
					roomsel = self.request.POST["room-delete"]
					room = Room.objects.get(id=roomsel)
					room.delete()
					
			except:
				pass


	#------------------
	def panel(self) :
	#------------------

		if self.request.session["panel"] == "roomcard"  :

			self.rg1 = RGNew(self.request)
			self.result["rg1"] = self.rg1
			roomlist = self.rg1.roomlister()
			for rl in roomlist :
				rl["vacant"] = []
				rl["occupied"] = []

				for item in rl["list"] :
					if item.current == 0 :
						rl["vacant"].append(item)
					else :
						rl["occupied"].append(item)		
						
			self.result["roomlist"] = roomlist

		if self.request.session["panel"] == "rsvncard"  :
			self.result['SchemeForm'] = SchemeForm()
			self.result['RsvnBlogForm'] = RsvnBlogForm()
		
		if self.request.session["rsvnid"] > 0 :
			self.result['blogList'] = RsvnBlog.objects.filter(rsvn__id=self.request.session['rsvnid']).order_by("-time")
			schemeForm = SchemeForm()
			try:
				scheme = Scheme.objects.get(rsvn__id=self.request.session['rsvnid'])
				schemeForm = SchemeForm(instance=scheme)
				self.result["schemecolor"] = scheme.gridColor
			except:
				pass
			self.result["SchemeForm"] =  schemeForm	
 			# setup Schema
			# setup Blog
	#------------------
	def load_rsvn(self) :
	#------------------
		if self.rsvnid  :
			try:	
				self.rsvn = Rsvn.objects.get(id=self.rsvnid)
				self.result['RsvnForm'] = RsvnForm(instance=self.rsvn)
				self.result["rsvn"] = self.rsvn
			except:	
				self.result['RsvnForm'] = RsvnForm()
				self.request.session["rsvnid"] = 0
				self.rsvnid = 0
		else :
			self.result['RsvnForm'] = RsvnForm()

	#------------------
	def init(self) :
	#------------------
		change = False
		self.sesvar = {"rsvnid":0,"panel":"welcomecard"}
		if "rsvnid" in self.request.POST :
			rsvnid = int(self.request.POST["rsvnid"])
			if int(rsvnid) == 0 :
				self.request.session["panel"] = "rsvncard"

			if self.request.session["rsvnid"] != rsvnid:
				change = True
		self.sesvar_set()
		self.request.session["rsvnid"] = int(self.request.session["rsvnid"])
		if change:
			self.request.session["panel"] = "rsvncard"
		self.rsvnid = self.request.session["rsvnid"]
		# make a list of the blogs



#================================================================================================
class RsvnCreate (VClass) :
#================================================================================================
	template_name = "revise/detailForm2.html"
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
		return render(request,self.template_name,self.result )

	# ==========================================================
	def loadBlankForm(self) :
		pass
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
		self.result["create"] = True
		if self.arg_check('saveForm') :
			self.loadEditForm()
		else:	 
			self.loadBlankForm()
#================================================================================================
class RsvnUpdate (VClass) :
#================================================================================================
	template_name = "revise/detailForm2.html"
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
				
		return render(request,self.template_name,self.result)

	#----------------------------------
	def main(self) :
	#----------------------------------
		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid
		

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
		#self.roomToggles()

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






