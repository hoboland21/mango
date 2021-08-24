from rsvn.tools.misc import *
from rsvn.tools.misc import *
from rsvn.models import *
from django.shortcuts import redirect
from rsvn.vctools.roomGrid import *
#from rsvn.vc import event,calendar,agent,chat
from django.utils.decorators import method_decorator
from rsvn.vc.vclass import VClass

from rsvn.vctools.tools import *



#=====================================================================
class EventView (VClass) :
#=====================================================================
	def main (self) :
		self.template_name = "revise/eventForm.html"
		
		self.event = SideEvent()
		self.event_form = SideEventForm(instance=self.event)
		self.event_list = SideEvent.objects.all()

		if self.arg_check('addEvent') :
			self.agentid = self.args_put['addEvent']
			self.addEvent()

		if self.arg_check('editEvent') :
			self.evid = self.args_put['editEvent']
			self.editEvent()

		if self.arg_check('updateEvent') :
			self.evid = self.args_put['updateEvent']
			self.updateEvent()

		if self.arg_check('deleteEvent') :
			self.evid = self.args_put['deleteEvent']
			event= SideEvent.objects.get(pk=self.evid)
			event.delete()

		
		
		
		
		self.result['eventForm'] = self.event_form
		self.result['eventList'] = self.event_list
		self.result['event'] = self.event

	#------------------------------
	def addEvent(self) :
	#------------------------------
		self.event_form = SideEventForm(self.args_put)

		if self.event_form.is_valid() :
			ev = self.event_form.save(commit=False)
			ev.clerk = self.request.user.username
			ev.save()

			self.event_form = SideEventForm()
	#------------------------------
	def editEvent(self) :
	#------------------------------
		self.event= SideEvent.objects.get(pk=self.evid)
		self.event_form = SideEventForm(instance=self.event)
		self.result['edit'] = '1'
		self.result['evid'] = self.evid
	
	#------------------------------
	def updateEvent(self) :
		self.event= SideEvent.objects.get(pk=self.evid)
		self.event_form = SideEventForm(self.args_put, instance=self.event)
		if self.event_form.is_valid() :
			self.event_form.save()
			self.event_form = SideEventForm()
			self.result['edit'] = '0'
		
			
			
			
			
