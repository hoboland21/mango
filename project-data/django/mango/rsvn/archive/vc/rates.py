from rsvn.vc.vclass import VClass
from time import clock
from rsvn.models import *
from datetime import date,timedelta,datetime
from django.db.models import Q

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class RatesView(VClass) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
		self.template_name = "revise/rates.html"
		
		self.args = {
			"rateid" : "0",
		}
		self.args_fix()

		self.rateid = self.args['rateid']
		
		# Check and if defaults not set let's get the rates system up
		
		self.basic_setup()
		self.arg_action()
		self.args_send()

		#===============================================

		self.result['rateHeadForm'] 	= self.rateHeadForm
		self.result['rateAtomForm']  	= self.rateAtomForm
		self.result['rateAtoms'] 		= self.rateAtoms
		self.result['rateid']			= self.rateid
		self.result['allRateHeads'] 	= self.allRateHeads
		self.result['seasonForm']		= self.seasonForm
		self.result['season']			= self.season
		self.result['seasonsList']		= self.seasonsList

	#----------------------------------------------------
	def basic_setup(self) :
	#----------------------------------------------------
		# send all rate names to HTML
		self.allRateHeads  = RateHeading.objects.all()

		# initialize all forms
		self.rateHead 		= RateHeading()
		self.rateAtom		= RateAtom()
	
		self.rateAtoms 		= [] 
		self.rateHeadForm 	= RateHeadingForm(instance=self.rateHead)
		self.rateAtomForm	= RateAtomForm(instance=self.rateAtom)
	
		# season
		self.seasonsList	= Season.objects.all()
		self.season			= Season()
		self.seasonForm		= SeasonForm(instance=self.season)
		
		
		# initialize rate system if not yet
		self.initRateHeading() 
#		self.initSeasons()
		
		
		
	
		# get our current rate or the default ready for display
		if RateHeading.objects.filter(pk__exact = self.rateid) :
			self.rateHead = RateHeading.objects.get(pk__exact = self.rateid )
			self.rateAtoms = RateAtom.objects.filter(rateheading__id__exact = self.rateid)
	
	#-------------------------------------------
	def initSeasons(self):
	#-------------------------------------------
		defaults = [
			[ 'Spring 2014', 		'low', 	'2014-04-01','2014-07-20'],
			[ 'Summer 2014', 		'high', '2014-07-21','2014-08-17'],
			[ 'Fall 2014', 			'low', 	'2014-08-18','2014-12-25'],
			[ 'Christmas 2014', 	'peak', '2014-12-25','2015-01-05'],
			[ 'New Years 2015', 	'high', '2015-01-05','2015-01-11'],
			[ 'Early 2015', 		'low', 	'2015-01-12','2015-02-14'],
			[ 'Chinese 2015 ', 		'high', '2015-02-15','2015-02-21'],
			[ 'Pre Spring 2015', 	'low', 	'2015-02-22','2015-03-24'],
			[ 'Spring 2015', 		'high', '2015-03-25','2015-04-05'],
			[ 'Summer 2015',		'low',	'2015-04-06','2015-07-20'],
		]
		for d in defaults :
			if not Season.objects.filter(beginDate__exact = d[2]) :
				s = Season(name=d[0],season=d[1],beginDate=d[2],endDate=d[3])
				s.save()
	
	#-------------------------------------------
	def initRateHeading(self) :
	#-------------------------------------------
		# Default Headings
		for val in RATEHEADING_DEFAULT_DICT.itervalues() :
			if not RateHeading.objects.filter(title__exact = val) :
				rh = RateHeading(title=val, descr=val)
				rh.save()

		# default services
		rhs = RateHeading.objects.get(title__exact = "SERVICE")			
		for serv in SERVICE_FIELDS :
			if not RateAtom.objects.filter(rateheading__exact=rhs.id, rateName__exact=SERVICE_FIELDS[serv]) :
				ra = RateAtom(rateheading =rhs,rateName=SERVICE_FIELDS[serv],rateType="SERVICE")
				ra.save()

		#DEFAULT TYPE FIELDS ARE MADE IN THE BEGINNING
		rhs = RateHeading.objects.all().exclude(title__exact = "SERVICE") 			 
		for rh in rhs :
			for type in ROOM_TYPE_CHOICES :
				if not RateAtom.objects.filter(rateheading__exact = rh.id, rateType__exact = type[0]) :
					rha = RateAtom(rateheading=rh, rateType= type[0], rateName= type[1])
					rha.save()					

	#----------------------------------------------------
	def arg_action(self) :
	#----------------------------------------------------
		
		# RATE MAINT

		if self.arg_check("newRateHeading") :
			self.rateHeadForm = RateHeadingForm(self.args_put)
			if self.rateHeadForm.is_valid() :
				rateHead = self.rateHeadForm.save(commit=False)
				if not RateHeading.objects.filter(title__exact =  rateHead.title) : 
					rateHead.save()
					self.rateHeadForm = RateHeadingForm()
				self.rateHead = rateHead		
		
		
		if self.arg_check("rateDelete") :
			rateHeading = RateHeading.objects.get(pk=self.rateid)
			if not RateAtom.objects.filter(rateheading_id__exact = rateHeading.id) :
				rateHeading.delete()
			self.rateHeadForm = RateHeadingForm()		
		
		
		# ATOM MAINT
		
		if self.arg_check("atomCreate") :
			self.rateAtomForm = RateAtomForm(self.args_put)
			if self.rateAtomForm.is_valid() :
				rateAtom = self.rateAtomForm.save(commit=False)
				rateHead = RateHeading.objects.get(id__exact = self.rateid)
			# no duplicate name
				if not RateAtom.objects.filter(rateheading__id__exact = self.rateid,
											     rateName__exact = rateAtom.rateName)  :
					rateAtom.rateheading = rateHead
					rateAtom.save()
					self.rateAtomForm = RateAtomForm()
				

		if self.arg_check("atomSelect") :
			rateAtom = RateAtom.objects.get(id__exact = self.args_put["atomSelect"])
			self.rateAtomForm = RateAtomForm(instance = rateAtom)
			self.result['atomid'] = rateAtom.id

		
		if self.arg_check("atomSave") :
			self.rateAtomForm = RateAtomForm(self.args_put)
			if self.rateAtomForm.is_valid() :
				rateAtom = RateAtom.objects.get(id__exact = self.args_put["atomSave"])
				self.rateAtomForm = RateAtomForm(self.args_put, instance=rateAtom)
				rateAtom = self.rateAtomForm.save(commit=False)
				rateHead = RateHeading.objects.get(id__exact = self.rateid)
				rateAtom.rateheading = rateHead
				rateAtom.save()
				self.result['atomid'] = self.args_put["atomSave"]


		if self.arg_check("atomDelete") :
			rateAtom = RateAtom.objects.get(id__exact = self.args_put["atomDelete"])
			rateAtom.delete()
			self.rateAtomForm = RateAtomForm()
		
		
		# Season MAINT
		
		if self.arg_check("seasonCreate") :
			self.seasonForm = SeasonForm(self.args_put)
			if self.seasonForm.is_valid() :
				season = self.seasonForm.save(commit=False)
				season.save()
				self.seasonForm = SeasonForm()
				

		if self.arg_check("seasonSelect") :
			season = Season.objects.get(id__exact = self.args_put["seasonSelect"])
			self.seasonForm = SeasonForm(instance = season)
			self.result['seasonid'] = season.id

		
		if self.arg_check("seasonSave") :
			self.seasonForm = SeasonForm(self.args_put)
			if self.seasonForm.is_valid() :
				season = Season.objects.get(id__exact = self.args_put["seasonSave"])
				self.seasonForm = SeasonForm(self.args_put, instance=season)
				season = self.seasonForm.save(commit=False)
				season.save()
				self.result['seasonid'] = self.args_put["seasonSave"]


		if self.arg_check("seasonDelete") :
			season = Season.objects.get(id__exact = self.args_put["seasonDelete"])
			season.delete()
			self.seasonForm = SeasonForm()






