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
from rsvn.vc.grid import *
from rsvn.vc.newMainGrid import *

#================================================================================================
class RsvnMain(RClass) :
#================================================================================================
	template_name = "revise/detailEditor.html"

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


		if self.request.session["panel"] == "gridcard"  :
			self.result["gridView"] = gridView(self.request.session)
			



		
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
		self.request.session["rsvnid"] = int(self.request.session["rsvnid"])
		if change:
			self.request.session["panel"] = "rsvncard"
		self.rsvnid = self.request.session["rsvnid"]
		# make a list of the blogs


