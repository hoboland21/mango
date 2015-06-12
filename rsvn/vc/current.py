
from rsvn.models import *

from rsvn.vc.vclass import VClass
from time import clock
from datetime import date,timedelta,datetime 
from rsvn.vc.grid import TypeNameList



VACANT 		= 0
OCCUPIED 	= 1
DIRTY 		= 2
CLEAN_SCHED = 3
OOC			= 4
BB			= 5

#==============================================================
# This is our housekeeping grid class
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class currentView(VClass) :
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	colorWheel = ['white','red','gray', 'yellow','black']

	#-------------------------------------------
	#-------------------------------------------
	def main(self) :
	#-------------------------------------------
	#-------------------------------------------

		self.template_name = "revise/current.html"
		self.result['tableTitle'] = "Current Room Status Information"
		self.today = datetime.today().date()
		
		self.rInfo = RoomInfo.objects.all()
		
	
		if self.arg_check('toggleRoom') :
			self.clicker(self.args_put['toggleRoom'])
		
		elif self.arg_check('brcUpdate') :
			self.update_to_present()
		
		elif self.arg_check('brcReset') :
			self.currentReset()
		
		if self.arg_check('viewArchive') :
			self.viewArchive()
		else :
			self.makeGrid()
		
		self.result['logs'] = CurrentLog.objects.all().order_by('id')

#-------------------------------------------
	def viewArchive(self) :
#-------------------------------------------

		currentLog =CurrentLog.objects.get(pk__exact = self.args_put['archive'])

		archiveList = currentLog.log.split(',') 

		archiveDict = {}

		for al in archiveList :
			if ":" in al :
				key,val = al.split(" : ")
				val = val.strip(",")
				archiveDict[key] = val
		
		self.rInfo = RoomInfo.objects.all()
		rInfoList = []

		for name in TypeNameList :
			tlist = self.rInfo.filter(type__exact=name[0]).order_by('number')
			rInfoList.append("<tr><th>{}</th></tr><tr><td>".format(name[1]))
			for t in tlist:
				acurrent = archiveDict[t.number]

				bgcolor = self.colorWheel[int(acurrent)]
				fgcolor = 'black'

				if bgcolor in ['black','red'] :
					fgcolor = 'yellow'
				rInfoList.append("<button value='{1}' name='toggleRoom' class='tcel' style='background-color:{0}; color:{2}' >{1}</button>".format(bgcolor,t.number,fgcolor))

			rInfoList.append("</td></tr>".format(name[1]))
		self.result['rInfoList'] = rInfoList
			

#-------------------------------------------
	def makeGrid(self) :
#-------------------------------------------
		self.rInfo = RoomInfo.objects.all()
		rInfoList = []
		for name in TypeNameList :
			tlist = self.rInfo.filter(type__exact=name[0]).order_by('number')
			rInfoList.append("<tr><th>{}</th></tr><tr><td>".format(name[1]))
			for t in tlist:

				bgcolor = self.colorWheel[t.current]
				fgcolor = 'black'

				if bgcolor in ['black','red'] :
					fgcolor = 'yellow'
				rInfoList.append("<button value='{1}' name='toggleRoom' class='tcel' style='background-color:{0}; color:{2}' >{1}</button>".format(bgcolor,t.number,fgcolor))

			rInfoList.append("</td></tr>".format(name[1]))
		self.result['rInfoList'] = rInfoList

	#-------------------------------------------
	def clicker(self,number) :
	#-------------------------------------------
		rInfo = RoomInfo.objects.get(number = number)
		curr = rInfo.current

		curr = (curr + 1) % len(self.colorWheel)
		rInfo.current = curr
		if self.request.user.has_perm('rsvn.delete_rsvn') :
			rInfo.save()

	#-------------------------------------------
	def currentReset(self) :
	#-------------------------------------------
		for ri in self.rInfo :
			if ri.current not in [ OOC, VACANT ] :
				ri.current = VACANT
				ri.save()
	#-------------------------------------------
	def logSet(self) :
	#-------------------------------------------

		logList = [] 

		for ri in self.rInfo :
			logList.append("{} : {},".format(ri.number,ri.current))

		log = "".join(logList)
		thisDate = date.today().isoformat()

		currentLog =CurrentLog.objects.filter(date__exact = thisDate)

		if currentLog :
			currentLog =CurrentLog.objects.get(date__exact = thisDate)
			currentLog.log = log
		else :	
			currentLog = CurrentLog(date=thisDate, log=log)

		currentLog.save()
		
	#-------------------------------------------
	def update_to_present(self) :
	#-------------------------------------------
		# fill roomlist our work list
		roomList = {}
		
		# we load our work list here
		for ri in self.rInfo :
			roomList[ri.number] = ri.current
			
		# start off by clearing all occupied rooms to vacant rooms
		for rl in roomList :
			if roomList[rl] == OCCUPIED :
				roomList[rl] = VACANT

		# get all occupied rooms and set occupied
		for rn in Room.objects.filter(rsvn__dateIn__lte = self.today,  rsvn__dateOut__gte = self.today ).exclude(rsvn__status__exact='cancel') :
			number = rn.roominfo.number
			if rn.rsvn.status == "checkin" :
				roomList[number] = OCCUPIED


		# get all checked rooms
		for rn in Room.objects.filter(rsvn__dateOut__exact = self.today,rsvn__status__exact = "checkout" ).exclude(rsvn__status__exact='cancel')  :
			number = rn.roominfo.number
			if roomList[number]  in [ OCCUPIED, VACANT ] :
				roomList[number] = DIRTY

		# compare rooms
		for rL in roomList :
			ri = RoomInfo.objects.get(number__exact = rL)
			if ri.current != roomList[rL] :
				ri.current = roomList[rL]
				ri.save()

		self.logSet()
		
		
		
		
		
		
		