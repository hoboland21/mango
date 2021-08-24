from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Form, Textarea, TextInput, HiddenInput
from django import forms
from datetime import *
from decimal import Decimal
from rsvn.models import *
#--------------------------------------------------------------------
class WebRsvnForm(ModelForm):
	class Meta:
		model= WebRsvn
		labels = {
			'firstname':'First Name',
			'lastname':'Last Name',
			'phone1':'Telephone' ,
			'adult':'Adult (12 yr+)',
			'child':'Child (4-11 yr)',
			'infant':'Infant (0-3 yr)' }
		exclude = ['dateIn','dateOut','rooms','type','inquiry','rsvn','response' ]	
#---------------------------------------------------------
class WebRsvnFinalForm(ModelForm):
	class Meta:
		model= WebRsvn
		labels = {
			'firstname'	:'First Name',
			'lastname'	:'Last Name',
			'phone1'	:'Telephone' ,
			'adult'		:'Adult (12 yr+)',
			'child'		:'Child (4-11 yr)',
			'infant'	:'Infant (0-3 yr)',
			'dateIn' 	: 'Date From',
			'dateOut' 	: 'Date To',
			'rooms' 	: 'Number of Rooms',
			'type' 		: 'Room Type' }

		exclude = ['inquiry','rsvn']
		
#--------------------------------------------------------------------
class RsvnForm(ModelForm):
	class Meta:
		model= Rsvn
		fields = '__all__'
		labels = { 'dateIn': 'Check In', 'dateOut' : 'Check Out'}
		widgets = {
			'dateIn'	:TextInput 	(attrs={'class':'datepicker'}),
			'dateOut'  :TextInput 	(attrs={'class':'datepicker'}),
			'notes'		:Textarea	(attrs={'cols': 20, 'rows': 2}),
			'clerk'		:TextInput  (attrs={'readonly':'readonly'}),
			'confirm'	:TextInput  (attrs={'readonly':'readonly'})
			}

#---------------------------------------------------------
class RateHeadingForm(ModelForm) :
	class Meta :
		model = RateHeading
		fields = '__all__'
#---------------------------------------------------------
class RateAtomForm(ModelForm) :
	class Meta :
		model = RateAtom
		exclude  = ['rateheading']


#--------------------------------------------------------------------
class AgentForm(ModelForm) :
	class Meta:
		fields = '__all__'
		model= Agent

#--------------------------------------------------------------------
class ServiceForm(ModelForm) :
	class Meta:
		model= Service

		fields= '__all__'
		labels ={
			'from_airport'	: 'From Airport Trans',
			'to_airport'	: 'To Airport Trans',
			'earlyin'		: 'Early Check In',
			'lateout' 		: 'Late Check Out',
			'connect' 		: 'Connecting Room',
			'dailymaid'		: 'Daily Maid Service',
			'extrabed'		: 'Extra Bed',
			'mango' 		: 'Mango Access'
		}

		exclude = ['rsvn']


#--------------------------------------------------------------------
class TourForm(ModelForm) :
	class Meta:
		model= Tour
		fields = '__all__'
		exclude = ['rsvn']
		widgets = {
			'arrive_time' 	:TextInput  (attrs={'class':'datetimepicker'}),
			'depart_time' 	:TextInput  (attrs={'class':'datetimepicker'}),
			'promo' 		:Textarea	(attrs={'cols': 20, 'rows': 2}),
			}


#--------------------------------------------------------------------
class SchemeForm(ModelForm) :
	class Meta:
		model= Scheme
		exclude = ['rsvn','rsvnColor','extraColor']
#---------------------------------------------------------
class RoomForm(ModelForm) :
	class Meta:
		fields = '__all__'
		model= Room

#---------------------------------------------------------
class EventForm(ModelForm) :
	class Meta:
		model= Event
		exclude = ['rsvn',]
		widgets = {
			'descr'			:Textarea	(attrs={'cols': 20, 'rows': 5, 'class' : 'leftjust' }),
			'dateStart'		:TextInput 	(attrs={'class':'datepicker'}),
			'dateEnd'		:TextInput 	(attrs={'class':'datepicker'}),
			'timeEnd'		:TextInput 	(attrs={'class':'timepicker'}),
			'timeStart'		:TextInput 	(attrs={'class':'timepicker'}),
			}

#---------------------------------------------------------
class SideEventForm(ModelForm) :
	class Meta:
		model= SideEvent
		fields = "__all__"
		widgets = {
			'descr'			:Textarea	(attrs={'cols': 20, 'rows': 5, 'class' : 'leftjust' }),
			'dateStart'		:TextInput 	(attrs={'class':'datepicker'}),
			'dateEnd'		:TextInput 	(attrs={'class':'datepicker'}),
			'timeEnd'		:TextInput 	(attrs={'class':'timepicker'}),
			'timeStart'		:TextInput 	(attrs={'class':'timepicker'}),
			}

#---------------------------------------------------------
class SeasonForm(ModelForm) :
	class Meta:
		model=Season
		fields = '__all__'
		widgets = {
			'beginDate'	:TextInput 	(attrs={'class':'datepicker'}),
			'endDate'	:TextInput 	(attrs={'class':'datepicker'}),
			}		

#---------------------------------------------------------
class InvoiceEntryForm(ModelForm) :
	class Meta :
		model = InvoiceEntry
		exclude = ['time','clerk']
	
#---------------------------------------------------------
class RsvnBlogForm(ModelForm) :
	class Meta:
		model= RsvnBlog
		exclude = ['rsvn','clerk','time']
		widgets = {
			'desc' :Textarea	(attrs={'cols': 25, 'rows': 2}),
			}
