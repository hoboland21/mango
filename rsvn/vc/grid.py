#from django.utils.decorators import method_decorator
from rsvn.models import *
from rsvn.tools.misc import *
#from rsvn.vctools.tools import *
from rsvn.vctools.packing import rsvnidPacker
from rsvn.vc.vclass import VClass
from rsvn.vctools.newGrid import *

from datetime import time, date
#from  time import clock
from django.db.models import Q


#---------------------------------------------------------
def getGridColor(rsvnid) :
#---------------------------------------------------------
	result = "White"
	if  Scheme.objects.filter(rsvn_id__exact=rsvnid):
		scheme = Scheme.objects.get(rsvn_id=rsvnid)
		result = scheme.gridColor
	return result
#===========================================
TypeNameList = [
	['standard', 		'Standard'],
	['deluxe', 			'Deluxe'],
	['pool_deluxe', 	'Pool Deluxe'],
	['lanai' , 			'Lanai'],
	['presidential',	'Presidential'],
	['manor', 			'Manor'],
	['suites',			'Suites'],
	]


#=====================================================================
class gridView(VClass)	 :
#=====================================================================
	# ---------------
	def main(self) :
	# ---------------

		self.validTypeList = ['standard','deluxe','pool_deluxe','lanai','presidential','manor','suites']

		self.rsvnid = int(self.kwargs['rsvnid'])
		self.result['rsvnid'] = self.rsvnid

		self.template_name = "revise/grid.html"
		self.collision = []
		
		self.args = { 
			"dateStart"	:  date.today().isoformat(),
			"dateEnd"	:  (date.today() + timedelta(days=10)).isoformat(),
			"push"		: 'all',
			"pgmarker"	:  date.today().isoformat(),
		}
		self.args_fix()



		# Limit what types we want to view
		if self.args['push'] not in ['all'] :
			self.validTypeList = [ self.args['push'],]

		# date controller
		#-------------------------------------------
		self.dateStart = datetime.strptime(self.args['dateStart'],"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.args['dateEnd'],"%Y-%m-%d")
		self.numDays = (self.dateEnd - self.dateStart).days + 1
		#-------------------------------------------
		# get the static room label filling self.RoomOrderList
		self.room_labels()
		# create the grid structure		
		self.GM = gridMatrix()	
		self.GM.dateSequenceX(self.dateStart,days=self.numDays, format="%a%n%m/%d")
		self.GM.loadY(self.RoomOrderList)
#--------------
		# Highlight Type headings
		self.markHeads()
		# select my records
		self.rsvn_select()
		# load up the grid
		self.loadGrid()
		
		self.loadLabelTools()

		# send record to the header
		if (self.rsvnid) > 0 :
			self.result['rsvnRec'] = rsvnidPacker(self.rsvnid)
			self.result['rsvnid']  = self.rsvnid
#--------------

		# when we are completed we send the grid for rendering
		self.result['gridHTML'] = self.GM.HTML()
		# send our session arguments out
		self.args_send()

	#---------------------------------------------------------
	def markHeads(self) :
	#---------------------------------------------------------
		# all types get a highlight
		for type in TypeNameList :
			if type[0] in self.validTypeList :
				self.GM.highlightRow(type[0])		

		#mark the current date
		if self.dateStart.date() <= datetime.today().date() and  self.dateEnd.date() >= datetime.today().date() :
			self.GM.gridList[self.GM.xDict[datetime.today().date().isoformat()]][0]['color'] = "green"
			
		
	#---------------------------------------------------------
	def room_labels(self) :
	#---------------------------------------------------------
		# put room numbers y room search labels
		# by stepping through SortOrderDict - it is sorted

		self.RoomOrderList = []

		for type in TypeNameList :
			if type[0] in self.validTypeList :
				roomList = RoomInfo.objects.filter(type__exact=type[0]).order_by('number')
				self.RoomOrderList.append(type)
				for room in roomList :
					self.RoomOrderList.append([room.number,room.number])
	#-------------------------------------------
	def rsvn_select(self):
	#-------------------------------------------
		self.rsvnListing = Rsvn.objects.filter(
			Q(dateIn__gte = self.dateStart,   dateIn__lte= self.dateEnd  )   |
			Q(dateOut__gt = self.dateStart,  dateOut__lt= self.dateEnd  )  |
			Q(dateIn__lte = self.dateStart,   dateOut__gte= self.dateEnd  )
			).exclude(status__exact='cancel')
		
		for rsvn in self.rsvnListing :
			rsvn.roomset = rsvn.room_set.all()
			if rsvn.scheme_set.all() :
				rsvn.scheme = rsvn.scheme_set.all()[0]
	#-------------------------------------------
	def fixCollisions(self):
	#-------------------------------------------
		# in collision we have [ date, roomNumber ]
		for coll in self.collision :
			crooms = self.rsvnListing.filter(room__roominfo__number__exact = coll[1],
				dateIn__lte = coll[0], dateOut__gte = coll[0]).order_by('dateIn')
			lastId = crooms[1].id
			lastColor = getGridColor(lastId)

			frontId	= crooms[0].id
			frontColor = getGridColor(frontId)

			code = ("                                            \
				<table class='splitcell'>                        \
					<tr><td style='background-color:{1}'> <a href='/rsvn/grid/{0}'>B</a></td>  \
						<td style='background-color:{3}'><a href='/rsvn/grid/{2}'>B</a></td>  \
					</tr></table> ".format(frontId,frontColor,lastId,lastColor) )
			self.GM.put("color",coll[0],coll[1],"White")
			self.GM.put("data", coll[0],coll[1],code)
			self.GM.put("title",coll[0],coll[1],"back to back")
	
	#-------------------------------------------
	def loadGrid(self):
	#-------------------------------------------
		# go through each reservation and spot information
		for rsvn in self.rsvnListing :
			
			start = max(rsvn.dateIn,self.dateStart.date())
			# where I start is fine.. it is the end that we need to work on
			if rsvn.dateOut < self.dateEnd.date() :
				end = rsvn.dateOut
			elif rsvn.dateOut == self.dateEnd.date() :
				end = self.dateEnd.date()	
			elif rsvn.dateOut > self.dateEnd.date() :
				end = self.dateEnd.date() + timedelta(days=1)
			
			# this keeps the span at the right length
			span = end - start 
			anchor = "<a href=/rsvn/grid/{} > O </a>".format(rsvn.id)
			tooltip = "{} {} in:{} out:{}".format( rsvn.firstname, rsvn.lastname, rsvn.dateIn, rsvn.dateOut)
			gridColor = "white"
			if rsvn.scheme :
				gridColor = rsvn.scheme.gridColor
			
			# we have to bump the counter by 1
			for offset in range(span.days) :
				tdate = (start + timedelta(days=offset)).isoformat()
				for r in rsvn.roomset :
					if r.roominfo.type in self.validTypeList :
						if self.GM.get("data",tdate,r.roominfo.number ) == "" :
							self.GM.put("data",tdate,r.roominfo.number,anchor )
							self.GM.put("color",tdate,r.roominfo.number,gridColor)
							self.GM.put("title",tdate,r.roominfo.number,tooltip)
						else :
							self.collision.append([tdate,r.roominfo.number ])
		self.fixCollisions()							
					
	#-------------------------------------------
	def loadLabelTools(self):
	#-------------------------------------------
		for cnt in range(self.GM.yLength):
			item =  self.GM.gridList[0][cnt]["data"]
			if RoomInfo.objects.filter(number__exact = item) :
				RI = RoomInfo.objects.filter(number__exact = item)
				self.GM.gridList[0][cnt]["title"] = "{} Beds".format(RI[0].beds)
		

	
