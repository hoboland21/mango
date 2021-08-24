from rsvn.vc.vclass import VClass
from time import clock
from rsvn.models import *
from rsvn.vctools.tools import *
from rsvn.vctools.calcs import *
from datetime import date,timedelta,datetime
from django.db.models import Q
from decimal import *

OCCUPANCY_TAX = Decimal('0.15')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class invoiceView(VClass) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
		self.template_name = "revise/invoice.html"
		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid
		self.rsvn  = Rsvn.objects.get(pk=self.rsvnid)
		self.result['rsvnRec'] = rsvnPacker(self.rsvn)
		self.result['tableTitle'] = "Reservation Invoice"
			
		#	see if there is an invoice for this reservation.. if not create it	
		#	result self.invoice
		self.checkInvoice()

		if self.arg_check('changeRate') :
			new_rate = self.args_put['rateChange']
			newrate =  RateAtom.objects.get(pk__exact =new_rate)
			self.invoice.rateName = newrate.rateName
			self.invoice.save()


		#   Check our date span get our season list	
		self.seasonCheck()

		#  grab the correct heading
		self.getRateHeading()

		#  grab the correct atom
		self.getRateAtom()
		
		
	
	
		
		# this is the Decimal tally
		self.grandTotal = Decimal('0')
		# here are the charges as list of list [ type name amount ] 
		self.chargeList = [ ]
		
		
		#calculate the room
		self.roomCalculate()
		#  Calculate service 	
		self.serviceCalculate()
		
		# Total Room Charge
		self.total_line_entry(["Grand Total", moneyfmt(self.grandTotal) ])
		self.result['chargeList'] = self.chargeList

		
		self.arg_action()
		
		
		self.argstoHTML()
	# list out services and the costs of each
	# once all calculated create a record of the invoice and store in our format
	
	

	#-------------------------------------------
	def getRateHeading(self) :		
	#-------------------------------------------
		#get our rate heading
		if 	self.rsvn.tour_set.all() :

			tour = self.rsvn.tour_set.all()[0]

			agentRate = AgentRate.objects.get(agent__exact = tour.agent)
			self.rateHeading = agentRate.rateheading
		else :
			self.rateHeading = RateHeading.objects.get(title__exact = RATEHEADING_DEFAULT_DICT[self.rsvn.source])
		
		# we have all of our rate atoms now
		self.rateAtoms = RateAtom.objects.filter(rateheading__exact=self.rateHeading.id)
		
	
	#-------------------------------------------
	def getRateAtom(self) :
	#-------------------------------------------
		# we need our rate atom
		current_name = self.invoice.rateName

		# make sure our ratename is valid
	
		if self.rateAtoms.filter(rateName__exact = current_name) :
			self.rateAtom = self.rateAtoms.filter(rateName__exact = current_name)[0]
		else :
			self.rateAtom = self.rateAtoms.filter(rateType__exact = self.rsvn.type)[0]
			current_name = self.rateAtom.rateName
			self.invoice.rateName = current_name
			self.invoice.save()

	#-------------------------------------------
	def argstoHTML(self) :	
	#-------------------------------------------
		# create a list of atoms with this type
		self.result['rateList'] = self.rateAtoms.filter(rateType__exact = self.rsvn.type)
		
		# send rate heading to html
		self.result['rateHeading'] = self.rateHeading
		
		#  rate atom to HTML	
		self.result['rateAtom'] = self.rateAtom
	
	
	#-------------------------------------------
	def roomCalculate(self) :
	#-------------------------------------------
			
		
		rateval = {
			'low': Decimal(self.rateAtom.lowSeason),
			'high': Decimal(self.rateAtom.highSeason),
			'peak': Decimal(self.rateAtom.peakSeason),
		}
		room_charge = Decimal('0')
		
		# count through the days in the season and calculte
		
		
		for sea in self.season :
			calc = Decimal(sea.days) * Decimal(rateval[sea.season])
			desc = "Room {} for {} Days {} @ {}".format(self.rsvn.type, sea.days, sea.name ,rateval[sea.season])
			
			room_charge += calc			
			
			self.line_entry([ "Room Charge", desc, sea.days,moneyfmt(rateval[sea.season]), moneyfmt(calc) ])

		# all room charges in room_charge
		
		# Sub Total Room Charge
		self.total_line_entry(["Room Sub Total", moneyfmt(room_charge) ])
		
		occ_tax = Decimal(room_charge) * OCCUPANCY_TAX
		
		# Occupancy tax
		self.total_line_entry([ "Occupancy Tax",moneyfmt(occ_tax) ])
		room_total = room_charge + occ_tax 

		# Total Room Charge
		self.total_line_entry([ "Total Room Charge", moneyfmt(room_total) ])
		
		# Running Grand Total moving on		
		self.grandTotal += room_total


	#-------------------------------------------
	def serviceCalculate(self) :
	#-------------------------------------------
		self.serviceRate = RateAtom.objects.filter(rateheading__title__exact = "SERVICE")
		if self.rsvn.service_set.all() :
			self.serviceList  = serviceSplitter(self.rsvn.service_set.all()[0])
			for serv in self.serviceList :
				rate = self.serviceRate.get(rateName__exact = serv[1])
				multi = Decimal('1')
				# we do the multiple for meals and
				if serv[0] in [ 'breakfast','lunch','dinner', 'dailymaid'] :
					multi = Decimal(self.rsvn.num_days())
				val = multi * rate.lowSeason
				
				self.grandTotal += val
				
				self.line_entry([ "Service", serv[1], multi, moneyfmt(rate.lowSeason), moneyfmt(val) ])

	#-------------------------------------------
	def line_entry(self,e) :
	#-------------------------------------------
		self.chargeList.append("<tr><td>{}</td><td>{}</td><td style='text-align:right'>{}</td><td  style='text-align:right'>{}</td><td  style='text-align:right'>{}</td></tr>".format(
			e[0],e[1],e[2],e[3],e[4]) )
				
	#-------------------------------------------
	def total_line_entry(self,e) :
	#-------------------------------------------
		self.chargeList.append("<tr><td  colspan='4' style='text-align:right'>{}</td> <td  style='text-align:right'>{}</td> </tr>".format(
			e[0],e[1]) )
		

	#-------------------------------------------
	def arg_action(self) :
	#-------------------------------------------
		pass
	#-------------------------------------------
	# check if invoice exists.. create it if not
	#-------------------------------------------
	def checkInvoice(self) :
	#-------------------------------------------
		if Invoice.objects.filter(rsvn_id__exact = self.rsvnid) :
			self.invoice = Invoice.objects.get(rsvn_id__exact = self.rsvnid)
		else :
			rateheading = RateHeading.objects.get(title = RATEHEADING_DEFAULT_DICT[self.rsvn.source])
			self.invoice = Invoice(rsvn=self.rsvn,rateheading=rateheading)
			self.invoice.save()
		
		
	#-------------------------------------------
	def seasonCheck(self):
	# we grab the applicable season(s) for this rsvn.. we make a list called self.season
	#-------------------------------------------
		self.season = Season.objects.filter(
			Q(beginDate__gte = self.rsvn.dateIn, beginDate__lte = self.rsvn.dateOut) |
			Q(beginDate__lte = self.rsvn.dateIn, endDate__gte = self.rsvn.dateIn) |
			Q(beginDate__lt = self.rsvn.dateOut, endDate__gte = self.rsvn.dateOut)
			)
		
		for seas in self.season :
			firstday = max(seas.beginDate,self.rsvn.dateIn)
			lastday = min(seas.endDate, self.rsvn.dateOut)
			
			seas.days = (lastday - firstday).days+1
			if lastday == self.rsvn.dateOut :
				seas.days += -1
		
		cnt = 0
		
		for seas in self.season :
			cnt += seas.days

'''
		transForm = TransForm()

		if self.arg_check('addTrans') :
			transForm = TransForm(self.args_put)
			if transForm.is_valid() :
				trans = transForm.save(commit=False)
				trans.clerk = self.request.user.username
				trans.invoice = Invoice.objects.get(pk=self.invoice)
				trans.save()


				
		if self.arg_check('delTrans') :
			transid = self.args_put['delTrans']
			trans = Trans.objects.get(id=transid)
			trans.delete()			


		if self.arg_check('editTrans') :
			transid = self.args_put['editTrans']
			trans = Trans.objects.get(id=transid)
			transForm = TransForm(instance=trans)
			self.result['transid'] = transid

		if self.arg_check('saveTrans') :
			transid = self.args_put['saveTrans']
			trans = Trans.objects.get(id=transid)
			transForm = TransForm(self.args_put, instance=trans)
			self.result['transid'] = transid

			if transForm.is_valid() :
				trans.clerk = self.request.user.username
				trans.time = datetime.now()
				trans.save()

		self.result['transForm'] = transForm

		
'''		
