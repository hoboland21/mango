#from rsvn.tools.misc import *
#from rsvn.vctools.roomGrid import *
#from rsvn.vc import event,calendar,agent,chat
#from rsvn.vctools.tools import *
#from rsvn.vctools.tools import *
from rsvn.models import *
from rsvn.forms import *
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from rsvn.v2.tools.vclass 	import *
from rsvn.v2.newMainGrid 	import *
from rsvn.v2.tools.roomStats import *
from rsvn.v2.tools.packing  import *
from rsvn.v2.tools.search  import *

#================================================================================================
class RsvnMain(RClass) :
#================================================================================================
	template_name = "detailEditor.html"

# ==========================================================
	#------------------
	def main(self) :
	#------------------
		#self.rsvn = Rsvn()
	
		# runtime init
		self.init()

		if "newrsvn" in self.request.POST :
			self.rsvnid = 0
			self.request.session["rsvnid"] = 0
			self.request.session["panel"] = "rsvncard"			

		elif "go_search" in self.request.POST:
			self.result.update(search_query(self.request.POST))
	

		elif "grid_id_select" in self.request.POST :
			self.rsvnid = self.request.POST["grid_id_select"]
			self.request.session["rsvnid"] = self.rsvnid
			self.request.session["panel"] = "rsvncard"			

		elif "room-select" in self.request.POST :
			if  len(rg1.rsvn_rooms) < self.rsvn.rooms :
				roomsel = self.request.POST["room-select"]
				ri = RoomInfo.objects.get(id=roomsel)
				room = Room(roominfo=ri,rsvn=self.rsvn,roomstatus="select")
				room.save()
				####rescan rooms



		self.creator()
		self.updater()
		self.load_rsvn()
		self.panel()
			


		self.result["session"] = self.request.session 
# ==========================================================
	#------------------
	def init(self) :
	#------------------
		self.RRStats = RsvnRoomStats(self.rsvn)
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
			self.result['roomlist'] = self.RRStats.roomlister() 
			self.result['rsvn_rooms'] = self.RRStats.rsvn_rooms
		

		if self.request.session["panel"] == "rsvncard"  :
			self.result['SchemeForm'] = SchemeForm()
			self.result['RsvnBlogForm'] = RsvnBlogForm()
			self.result['rsvn_rooms'] = self.RRStats.rsvn_rooms


		if self.request.session["panel"] == "gridcard"  :
			self.result["gridView"] = gridView(self.request.session)

		if self.request.session["panel"] == "currentcard"  :
			# We will put out lister of room status
			ridc = RoomInfoDisplayCtrl()
			self.result["currentView"]  = ridc.listing()

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

