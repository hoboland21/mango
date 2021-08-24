
#from rsvn.tools.misc import *
from rsvn.models import *

from django.views.generic.base import View
from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

#from rsvn.vctools.tools import *
from rsvn.v2.tools.newGrid import *

#=====================================================================
class RClass (View)	 :
#=====================================================================
	# Reservation Class will automatically set up
	# dateIn dateOut rsvnid making it available
	# ---------------
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs) :
	# ---------------
		self.request = request
		self._init()
		self.main()
		return render(self.request,self.template_name,self.result )

	# ---------------
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.request = request
		self._init()
		self.main()
		return render(self.request,self.template_name,self.result)

	#============================
	def _init(self):
	#============================
		self.result = {}
		self.change =  False
		self.today = date.today().isoformat()
		self.tomorrow =  (date.today() + timedelta(days=10)).isoformat()

		dataset = {
			"rsvnid"	:0,
			"dateStart"	:self.today,
			"dateEnd"	:self.tomorrow,
			'panel'		:'welcomecard' }

		for k,v in dataset.items() :
			if k not in self.request.session :
					self.request.session[k] = v

		# if we are bringing an rsvnid in through post push to session
		if "rsvnid" in self.request.POST :
			rsvnid = int(self.request.POST["rsvnid"])
			# if the session and the post rsvnid are different 
			# we are making a reservation change
			if self.request.session["rsvnid"] != rsvnid:
				self.change = True
				# session update 
				self.request.session["rsvnid"]=rsvnid

		# set self rsvn and load the reservation		
		self.request.session["rsvnid"] = int(self.request.session["rsvnid"])
		# any changesto rsvn id automatically gives rsvncard
		if self.change:
			self.request.session["panel"] = "rsvncard"

		# fix rsvnid
		self.rsvnid = self.request.session["rsvnid"]
		
		# load the reservation in
		self.rsvn = Rsvn()
		if self.rsvnid :
			self.rsvn = Rsvn.objects.get(id=self.rsvnid)



#		if rsvnid == 0 || self.change  :
#			self.request.session["panel"] = "rsvncard"

'''

#=====================================================================
class SmallVClass (View)	 :
#=====================================================================

	form_class = ""
	result ={}
	request = ""
	# sesvar is array of key:default 
	sesvar = {}

	# ---------------
	def main(self) :
	# ---------------
		pass


	# ---------------
	def sesvar_set(self):
	# ---------------
		for k in self.sesvar :
			if k in self.request.POST :
				x = self.request.POST[k] 
				self.request.session[k] = x
			else:	
				if k not in self.request.session :
					self.request.session[k] = self.sesvar[k]
			self.result[k] = self.request.session[k]
		self.result["session"] = self.request.session		




	# ---------------
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs) :
	# ---------------
		self.request = request
		self.main()
		return render(self.request,self.template_name,self.result )

	# ---------------
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.request = request
		self.main()
		return render(self.request,self.template_name,self.result)

#=====================================================================
class VClass (View)	 :
#=====================================================================

	form_class = ""
	result ={}
	request = ""
	args_put = {}
	args_get = {}
	args = {}				

	# ---------------
	def main(self) :
	# ---------------
		pass
		
	#-------------------------------------------------------
	def args_fix (self) :
	#-------------------------------------------------------
		# our session args
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


	# ---------------
	def arg_check(self,arg) :
	# ---------------
		if arg in self.args_put :
			return True
		return False

	#-------------------------------------------------------
	def args_send(self) :   # send args back to result and session
	#-------------------------------------------------------
		for arg in self.args :
			self.result[arg] = self.args[arg]
			self.request.session[arg] = self.args[arg]


	# ---------------
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs) :
	# ---------------
		self.args_put = request.POST
		self.request = request
		self.main()
		
		return render(self.request,self.template_name,self.result )

	# ---------------
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.args_get = request.GET
		self.request = request
		self.main()
		return render(self.request,self.template_name,self.result)


#=====================================================================
class UVClass (View)	 :
#=====================================================================

	form_class = ""
	result ={}
	request = ""
	args_put = {}
	args_get = {}
	args = {}				

	# ---------------
	def main(self) :
	# ---------------
		pass
		
	#-------------------------------------------------------
	def args_fix (self) :
	#-------------------------------------------------------
		# our session args
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


	# ---------------
	def arg_check(self,arg) :
	# ---------------
		if arg in self.args_put :
			return True
		return False

	#-------------------------------------------------------
	def args_send(self) :   # send args back to result and session
	#-------------------------------------------------------
		for arg in self.args :
			self.result[arg] = self.args[arg]
			self.request.session[arg] = self.args[arg]


	# ---------------
	def post(self, request, *args, **kwargs) :
	# ---------------
		self.args_put = request.POST
		self.request = request
		self.main()
		
		return render(self.request,self.template_name,self.result)

	# ---------------
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.args_get = request.GET
		self.request = request
		self.main()
		return render(self.request,self.template_name,self.result )

'''
