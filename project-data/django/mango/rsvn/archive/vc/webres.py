from rsvn.vc.vclass import *
from rsvn.models import *
from rsvn.vc.detailEdit import RsvnCreate
from rsvn.vctools.tools import *



RSVNFIELDS = [
	'status','firstname','lastname','source',
	'phone1','phone2','dateIn','dateOut','rooms',
	'type','beds','adult','child','infant','notes',
	'city','country','email','confirm','clerk'
]



#=====================================================================
class WebResView (VClass)	 :
#=====================================================================
	def main (self) :
		self.template_name = "webview/webres.html"
		self.result['rsvnentry'] = "off"
		
		if self.arg_check('deleteRecord') :
			webrec = WebRsvn.objects.get(pk=self.args_put['deleteRecord'])
			webrec.delete()

		self.wrsvn = WebRsvn()
		self.wrsvnForm = WebRsvnForm(instance=self.wrsvn)
		self.wrsvnList = WebRsvn.objects.all()

			
		self.result['wrsvnList'] = self.wrsvnList 	
		

#=====================================================================
class WebMake (VClass) :
#=====================================================================
	def main(self) :
		self.template_name = "webview/webres.html"
		self.webid = int(self.kwargs['webid'])
		self.result['rsvnentry'] = "on"
		self.result['webid'] = self.webid

		self.wrsvn = WebRsvn.objects.get(pk=self.webid)

		self.saveWeb()

	# ---------------
	def post(self, request, *args, **kwargs) :
	# ---------------
		self.args_put = request.POST
		self.request = request
		self.rsvnid = 0
		self.main()
		if self.rsvnid > 0 :
			return redirect('rsvnupdate', self.rsvnid )
			
		return render(self.template_name,self.result, context_instance=RequestContext(request) )
#--------------------------------------------------------
	def saveWeb(self) :
#--------------------------------------------------------
		if self.arg_check('saveRsvn') :
			self.rsvnForm = RsvnForm(self.args_put)
			if self.rsvnForm.is_valid() :
				rsvn =  self.rsvnForm.save(commit=False)
				rsvn.save()
				rsvn.clerk = self.request.user.username
				rsvn.confirm = confirm_gen(rsvn.id)
				rsvn.save()			
				self.wrsvn.rsvn = rsvn.id
				self.wrsvn.save()
				
				scheme=Scheme(rsvn=rsvn)
				scheme.save()
				service=Service(rsvn=rsvn)
				service.save()
				self.rsvnid = rsvn.id
		else :	
			names = self.wrsvn._meta.get_all_field_names()
			rsvn = Rsvn()
			for field in names :
				if field in RSVNFIELDS :
					value = getattr(self.wrsvn,field,None)
					if field == 'type' :
						value = ROOM_TYPE_DICT_REV[value]
					setattr(rsvn, field, value)
			self.rsvnForm = RsvnForm(instance=rsvn)
		self.result['rsvnForm'] =  self.rsvnForm

'''
		
			
#=====================================================================
class WebMailView (VClass)	 :
#=====================================================================
	def main(self) :
		self.template_name = "webview/webmail.html"
		self.webid = int(self.kwargs['webid'])
		self.result['webid'] = self.webid
		self.wrsvn = WebRsvn.objects.get(pk=self.webid)
		self.wrsvnForm = WebRsvnForm(instance=self.wrsvn)
		self.result['wrsvnForm'] = self.wrsvnForm

		if self.arg_check('send') :
			self.webmailForm = WebMailForm(self.args_put)
			if self.webmailForm.is_valid() :
				webMail =  self.webmailForm.save(commit="no")
				webMail.save()
#				mail(webMail)
		else :	
			self.webMail 		= 	WebMail()
			self.webMail.date	=	datetime.now().date().isoformat()
			self.webMail.to	 	= 	self.wrsvn.email
			self.webMail.clerk	=	self.request.user
			self.webMail.wrsvn	=   self.wrsvn.id
			self.webMail.sender	=	"book@mangoresort.com"
			self.webmailForm 	= 	WebMailForm(instance=self.webMail)

		self.result['webmailForm'] = self.webmailForm
	
		self.webMailList = WebMail.objects.filter(wrsvn = self.webid)
		
		self.result['msgList'] =  self.webMailList
		self.MakeRsvn()
#------------------------------------------------------
	def MakeRsvn(self) :
#------------------------------------------------------
		names = self.wrsvn._meta.get_all_field_names()
		rsvn = Rsvn()
		for field in names :
			if field in RSVNFIELDS :
				value = getattr(self.wrsvn,field,None)
				setattr(rsvn, field, value)
				print field ," = ",value
		self.result['rsvnForm'] =  RsvnForm(instance=rsvn) 
		




'''