#from django.views.generic.base import View
#from django.utils.decorators import method_decorator

from rsvn.views import *
from datetime import time, date

#from rsvn.vctools.calClass import *
from rsvn.vctools.tools import *

from rsvn.vctools.newGrid import *

from rsvn.vc.vclass import VClass


from django.utils import timezone
import pytz

from decimal import *


#=====================================================================
class ExcelView (VClass) :
#=====================================================================

	# ---------------
	def main(self) :
	# ---------------
		self.template_name = "revise/excelview.html"
		
		self.args = { 
			"dateStart"	:  date.today().isoformat(),
			"dateEnd"	:  (date.today() + timedelta(days=10)).isoformat(),
		}

		self.args_fix()

		self.dateStart = datetime.strptime(self.args['dateStart'],"%Y-%m-%d")
		self.dateEnd = datetime.strptime(self.args['dateEnd'],"%Y-%m-%d")
		self.numDays = (self.dateEnd - self.dateStart).days + 1

		self.roomInfoList = RoomInfo.objects.all().order_by('number')

		roomlist = Room.objects.filter(
			Q(rsvn__dateIn__gte = self.dateStart,  rsvn__dateIn__lte= self.dateEnd  )   |
			Q(rsvn__dateOut__gt = self.dateStart,  rsvn__dateOut__lt= self.dateEnd  )  |
			Q(rsvn__dateIn__lte = self.dateStart,   rsvn__dateOut__gte= self.dateEnd  )
			).exclude(rsvn__status__exact='cancel')

		# roomlist has current rooms
		for rl in self.roomInfoList :
			rl.guest = roomlist.filter(roominfo__number__exact=rl.number )



		self.args_send()
	
		self.result['roomListing']= self.roomInfoList
