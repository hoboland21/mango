
from rsvn.tools.misc import *
from rsvn.models import *

from django.views.generic.base import View
from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

from rsvn.vctools.tools import *
from rsvn.vctools.newGrid import *


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
		
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )

	# ---------------
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.args_get = request.GET
		self.request = request
		self.main()
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )


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
		
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )

	# ---------------
	def get(self, request, *args, **kwargs) :
	# ---------------
		self.args_get = request.GET
		self.request = request
		self.main()
		return render_to_response(self.template_name,self.result, context_instance=RequestContext(request) )

