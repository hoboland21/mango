from django.shortcuts import  get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from collections import defaultdict
from django.utils.timezone import utc
import string
import calendar
import random
from django.template import RequestContext
from datetime import timedelta, date, time, datetime

# Create your views here.
from rsvn.models import *
from rsvn.vc.vclass import *
from rsvn.vctools.tools import *
from decimal import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#--------------------------------------------------------
def mail(webRsvn) :
#--------------------------------------------------------

	message = "\n".join([
		"This is an automated response from Mango Resort.",
		"We have received your inquiry No. {}".format(webRsvn.inquiry),
		"A representative will contact you within the next 24hours",
		"",
		"Thank You",
		" The Mango Team"
		])

	msg = MIMEText(message)
	msg['Subject'] = "Reservation Inquiry"
	msg['From'] = "Mango Resort Saipan"

	msg['To'] = "{} {}".format(webRsvn.firstname,webRsvn.lastname)
	
	
	s = smtplib.SMTP()
	s.connect('mangoresort.com')	
	s.login('jc@mangoresort.com','pimil210')
	
	me = "book@mangoresort.com"

	sendlist = [ webRsvn.email, "jc@mangoresort.com", "jc@saipantech.com"]

	s.sendmail(me, sendlist, msg.as_string())

	s.quit()
	
#-------------------------------------------------------
def web_confirm_gen () :
#-------------------------------------------------------
	# Random Generator
	id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	today = date.today()
	return 'W{:04}{:02}{:02}{}'.format(today.year,today.month,today.day,id)
#=====================================================================
class webThanks(UVClass):
#=====================================================================
	#----------------------------------
	def post(self, request, *args, **kwargs) :
	#----------------------------------
		self.escape = 0
		self.args_put = request.POST
		self.request = request
		self.main()
		if self.escape == 1 :
			return redirect ('http://themangoresort.com:88')
				
		return render(self.template_name,self.result, context_instance=RequestContext(request) )	
	#-----------------------------------------
	def main(self):
	#-----------------------------------------
		self.webid = int(self.kwargs['webid'])
		self.template_name = "webview/webview_final.html"
		
		self.webRsvn = WebRsvn.objects.get(pk=self.webid)
		self.webRsvnForm = WebRsvnFinalForm(instance=self.webRsvn)
		self.result['theme_back'] = "white"
		self.result['theme_text'] = "#00572F"
		self.result['theme_accent'] = "#00572F"
		self.result['theme_orange'] = "#F99423";
		self.result['homeURL'] = "http://themangoresort.com:88"
		
		self.result['webRsvnForm'] = self.webRsvnForm
		self.result['webRsvn'] = self.webRsvn
		



#=====================================================================
class webView(UVClass):
#=====================================================================
	#----------------------------------
	def post(self, request, *args, **kwargs) :
	#----------------------------------
		self.escape =																																 0
		self.args_put = request.POST
		self.request = request
		self.main()

		if self.escape == 1 :
			return redirect ('webthanks', self.webRsvn.id)

		return render(self.template_name,self.result, context_instance=RequestContext(request) )	
	
	
	
	#-----------------------------------------
	def main(self):
	#-----------------------------------------
		self.availList = []
		self.roomDict ={} 
		self.ROOMTYPES = []
		self.OccTax = Decimal('1.15')
		
		self.template_name = "webview/webview.html"
		# these are session and received arguments... part of vclass
		self.args = { 
			"dateFrom"	:  date.today().isoformat(),
			"dateTo"	:  (date.today() + timedelta(days=10)).isoformat(),
			"typeChoice" : "Standard",
			"numRooms"   : "1"
		}
		self.args_fix()

		if 'type' in self.args_get :
			print "reading value from GET"
			self.args['typeChoice'] =  ROOM_TYPE_DICT[self.args_get['type']]
			

		for rtype in ROOM_TYPE_CHOICES :
			if rtype[0] not in [ 'manor','suites' ] :
				self.ROOMTYPES.append(rtype[1])
				self.roomDict[rtype[0]] = rtype[1]

		self.dateTo = datetime.strptime(self.args['dateTo'],"%Y-%m-%d").date() 
		self.dateFrom =  datetime.strptime(self.args['dateFrom'],"%Y-%m-%d").date() 
		self.numDays = (self.dateTo - self.dateFrom).days

		
	# action ---------------------------------		
		# lets get our season range 
		self.season = seasonCheck(self.dateFrom,self.dateTo)
		
		# get our availability count in that data range
		self.availRooms = availRooms(self.dateFrom,self.dateTo)
		
		# lets get rate sheet for Tour FIT
		rateHead = RateHeading.objects.get(title__exact="Tour FIT")
		self.rateAtoms = rateHead.rateatom_set.all()
		
		# we have the Atoms 

		self.makeCharge()
		
		choice = self.args['typeChoice']
		self.result['continue'] = 0
		if self.availList[choice]['avail'] == "Available" :
			self.result['continue'] = 1


		self.rsvnMake()
				
		self.result['ROOMTYPES'] = self.ROOMTYPES
		self.result['alist'] = self.availList  
	# ---------------------------------		
		self.args_send()
		self.result['info'] = {}
		self.result['info'].update(self.args)
		total = self.availList[self.args['typeChoice']]['total']
		self.result['info'].update( {
			"numDays" : self.numDays,
			"total"	  : total,
		})
	# ---------------------------------		
	# list for select options
		self.result['RoomTypeChoices'] = self.ROOMTYPES
	# color of theme background
	#	self.result['theme_back'] = "#00572F"
		self.result['theme_back'] = "white"
		self.result['theme_text'] = "#00572F"
		self.result['theme_accent'] = "#00572F"
		self.result['theme_orange'] = "#F99423";
		self.result['homeURL'] = "http://themangoresort.com:88"
		self.result.update (csrf(self.request))
		self.result.update(self.args)

	#-----------------------------------------
	def finalizeMake(self) :
	#-----------------------------------------
		self.webRsvnForm  = WebRsvnForm(self.args_put)
		if self.webRsvnForm.is_valid() :
			webRsvn 		= 	self.webRsvnForm.save(commit=False)
			webRsvn.dateIn 	= 	self.args['dateFrom']
			webRsvn.dateOut = 	self.args['dateTo']
			webRsvn.rooms 	=	self.args['numRooms']
			webRsvn.type	= 	self.args['typeChoice']
			webRsvn.inquiry=  web_confirm_gen()
			webRsvn.save()
			mail(webRsvn)		
			self.webRsvn = webRsvn 
			self.escape  = 1

	#-----------------------------------------
	def rsvnMake(self) :
	#-----------------------------------------
		self.result['next'] = 0
		if self.arg_check("bookRoom") :
			self.result['next'] = 1
			self.finalizeMake()
		
		else :
			if self.arg_check('next') :
				if self.args_put['next'] == '1' :
					self.result['next'] = 1
		
			self.webRsvnForm  = WebRsvnForm()
		
		
		self.result['webRsvnForm'] = self.webRsvnForm
		
	#-----------------------------------------
	def makeCharge(self) :
	#-----------------------------------------
		res = {}
		order = 0
		for Rtype in ROOM_TYPE_CHOICES :
			total = Decimal('0')
			rateAtom = self.rateAtoms.get(rateType__exact=Rtype[0])
			for season in self.season :
				rateval = {
					'low': Decimal(rateAtom.lowSeason),
					'high': Decimal(rateAtom.highSeason),
					'peak': Decimal(rateAtom.peakSeason),
				}
				total += rateval[season.season] * self.numDays

			# calculate in Occupancy Tax
			#  Remove Tax Bump   total *= self.OccTax	
			
			# Subtract requested Rooms  from available
			rmsLeft = int(self.availRooms[Rtype[0]]) - int(self.args['numRooms'])
			
			# data result dictionary			
			res[Rtype[1]] = {} 
			if rmsLeft >= 0 :
				res[Rtype[1]]['avail'] = "Available"
				res[Rtype[1]]['total'] = moneyfmt(total * int(self.args['numRooms']))
			else :
				res[Rtype[1]]['avail'] = "Not Available"
				res[Rtype[1]]['total'] = " -- "

		self.availList = res



