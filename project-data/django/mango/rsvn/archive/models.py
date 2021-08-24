from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Form, Textarea, TextInput, HiddenInput
from django import forms
from datetime import *
from decimal import Decimal
from rsvn.lists import * 

#---------------------------------------------------------
class WebRsvn (models.Model):

	firstname	=	models.CharField(max_length=30)
	lastname 	=	models.CharField(max_length=30)

	phone1 		=	models.CharField(max_length=20)

	email 		= 	models.EmailField()

	dateIn		=	 models.DateField()
	dateOut		=	 models.DateField()

	rooms		=  	models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	type		=  	models.CharField(max_length=15 )
	beds		= 	models.IntegerField(default=2,validators = [ MinValueValidator(1) ])
	
	adult		=	 models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	child		=	 models.IntegerField(default=0,validators = [ MinValueValidator(0) ])
	infant		=	 models.IntegerField(default=0,validators = [ MinValueValidator(0) ])

	city 		= 	models.CharField(max_length=30,blank=True)
	country 	= 	models.CharField(max_length=30)
	inquiry		=   models.CharField(max_length=20, blank=True)
	rsvn		=	models.IntegerField(default=0)

	def num_days (self):
		return  (self.dateOut - self.dateIn).days

	def __str__(self):
		fullname = "%s %s  %s - %s" % (self.firstname, self.lastname,self.dateIn, self.dateOut )
		return(fullname)

#---------------------------------------------------------
class Rsvn (models.Model):
	status		=	 models.CharField(max_length=13, choices=RESERVATION_STATUS)

	firstname	=	models.CharField(max_length=30)
	lastname 	=	models.CharField(max_length=30)

	confirm		=   models.CharField(max_length=20, blank=True)
	clerk		=   models.CharField(max_length=20, blank=True)

	source  	=	 models.CharField(max_length=20, choices=SOURCE_CHOICES)
	phone1 		=	models.CharField(max_length=20)
	phone2 		=	models.CharField(max_length=20, blank=True)

	dateIn		=	 models.DateField()
	dateOut		=	 models.DateField()

	rooms		=  	models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	type		=  	models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES)
	beds		= 	models.IntegerField(default=2,validators = [ MinValueValidator(1) ])
	
	adult		=	 models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	child		=	 models.IntegerField(default=0,validators = [ MinValueValidator(0) ])
	infant		=	 models.IntegerField(default=0,validators = [ MinValueValidator(0) ])


	city 		= 	models.CharField(max_length=30,blank=True)
	country 	= 	models.CharField(max_length=30)

	email 		= 	models.EmailField(blank=True)


	notes		=	models.TextField(blank=True)

	def num_days (self):
		return  (self.dateOut - self.dateIn).days

	def __str__(self):
		fullname = "%s %s  %s - %s" % (self.firstname, self.lastname,self.dateIn, self.dateOut )
		return(fullname)

#--------------------------------------------------------------------
class RateHeading(models.Model) :
	title		=	models.CharField(max_length=256)
	descr		=	models.CharField(max_length=1028)

	def __str__(self):
		return(self.title)		

	
#---------------------------------------------------------
class RateAtom(models.Model):
	rateheading =   models.ForeignKey(RateHeading,on_delete=models.CASCADE)
	rateName	=	models.CharField(max_length=512, blank=True)
	rateType	=  	models.CharField(max_length=128, choices=RATE_TYPE_CHOICES)
	lowSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	highSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	peakSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	
	def __str__(self):
		return(self.rateName)
#---------------------------------------------------------
class Agent (models.Model):
	agency			=	models.CharField(max_length=30)
	contact			= 	models.CharField(max_length=30, blank=True)
	telephone		= 	models.CharField(max_length=20, blank=True)
	fax			= 	models.CharField(max_length=20, blank=True)
	email 			= 	models.EmailField(blank=True)
	notes			=	models.TextField(blank=True)


	def __str__(self):
		return self.agency

	class Meta:
		ordering = ["agency"]
#--------------------------------------------------------------------
class AgentRate(models.Model) :
	agent 			= 	models.ForeignKey(Agent,on_delete=models.CASCADE)
	rateheading		=	models.ForeignKey(RateHeading,on_delete=models.CASCADE)
#--------------------------------------------------------------------
class Service (models.Model):
	rsvn			= 	models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	breakfast		=	models.BooleanField(default=False)
	lunch			=	models.BooleanField(default=False)
	dinner			=	models.BooleanField(default=False)
	from_airport	=	models.BooleanField(default=False)
	to_airport		=	models.BooleanField(default=False)
	dailymaid		=	models.BooleanField(default=False)
	mango			=	models.BooleanField(default=False)
	extrabed		=	models.BooleanField(default=False)
	crib			=	models.BooleanField(default=False)
	connect			=	models.BooleanField(default=False)
	earlyin			=	models.BooleanField(default=False)
	lateout			=	models.BooleanField(default=False)
	event			=	models.BooleanField(default=False)
#--------------------------------------------------------------------
class Tour (models.Model):
	agent			= 	models.ForeignKey(Agent,on_delete=models.CASCADE)
	rsvn			= 	models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	arrive_flight	= 	models.CharField(max_length=30, blank=True)
	arrive_time		=	models.DateTimeField()
	depart_flight	= 	models.CharField(max_length=30, blank=True)
	depart_time		=	models.DateTimeField()
	promo			=	models.TextField(blank=True)

	def __str__(self) :
		return "{} - {}".format(self.agent.agency, self.arrive_time)
#--------------------------------------------------------------------
class Scheme (models.Model):
	rsvn		= 	models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	gridColor 	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	rsvnColor   = 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	extraColor	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	def __str__(self):
		gC = "{} - {}  {}  {}".format(self.rsvn.firstname, self.gridColor, self.rsvnColor, self.extraColor )
		return(gC)
#--------------------------------------------------------------------
class RoomInfo (models.Model):
	number		=	models.CharField(max_length=5)
	type		=	models.CharField(max_length=25, choices=ROOM_TYPE_CHOICES)
	beds		=	models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	connect	 	=   models.CharField(max_length=5, blank=True)
	notes		=	models.TextField(blank=True)
	current		=	models.IntegerField(default=0)

	class Meta:
			ordering = ['number']

	def __str__(self):

		fullname = "Room %s - %s - %s Beds" % (self.number, self.type,self.beds )
		return(fullname)
	def currentText(self):
		return roomStateDict[self.current]	
#---------------------------------------------------------
class Room (models.Model):
	rsvn		=    models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	roominfo 	=	 models.ForeignKey(RoomInfo,on_delete=models.CASCADE)
	info		=  	 models.CharField(max_length=512, blank=True)
	roomstatus	=	 models.CharField(max_length=13, choices=ROOM_STATUS,blank=True)

	
	def __str__(self):
		fullname = "%s %s" % (self.rsvn,self.roominfo )
		return(fullname)

#---------------------------------------------------------
class Event(models.Model) :
	rsvn		= models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	title		= models.CharField(max_length=128)
	pax			= models.IntegerField(validators = [ MinValueValidator(1) ])
	descr		= models.TextField()
	venue 		= models.CharField(max_length=90,choices=VENUE_CHOICES)
	dateStart	= models.DateField( )
	timeStart	= models.TimeField( default = "00:00:00")
	dateEnd		= models.DateField( )
	timeEnd		= models.TimeField( default = "00:00:00")

#---------------------------------------------------------
class SideEvent(models.Model) :
	title		= models.CharField(max_length=128)
	pax			= models.IntegerField(validators = [ MinValueValidator(1) ])
	descr		= models.TextField()
	venue 		= models.CharField(max_length=90,choices=VENUE_CHOICES)
	dateStart	= models.DateField( )
	timeStart	= models.TimeField( default = "00:00:00")
	dateEnd		= models.DateField( )
	timeEnd		= models.TimeField( default = "00:00:00")
	class Meta:
		ordering=['-dateStart']

#---------------------------------------------------------
class Season(models.Model) :
	name		=	models.CharField(max_length=140)
	season		= 	models.CharField(max_length=40, choices=SEASON_LEVEL )
	beginDate	=	models.DateField()
	endDate		=	models.DateField()
	def __str__(self):
		return(self.name)

#---------------------------------------------------------
class CurrentLog(models.Model) :
	date		= models.DateField(unique=True)
	log			= models.TextField()

#---------------------------------------------------------
class Invoice(models.Model) :
	rsvn			= 	models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	rateheading 	=	models.ForeignKey(RateHeading,on_delete=models.CASCADE)
	rateName		=	models.CharField(max_length=512)
	number			=	models.CharField(max_length=100)
	date_created	=	models.DateField(auto_now=True)
	date_sent		= 	models.DateField(default=date(2010,1,1) )
	date_paid		=	models.DateField(default=date(2010,1,1) )
	text_record		=	models.TextField(blank=True)

#---------------------------------------------------------
class InvoiceEntry(models.Model) :
	invoice	= 	models.ForeignKey(Invoice,on_delete=models.CASCADE)
	clerk	= 	models.CharField(max_length=40)
	time	= 	models.DateTimeField(auto_now=True)
	type   	= 	models.CharField(max_length=64)
	desc	=	models.CharField(max_length=256)
	cost	=	models.DecimalField(max_digits=12, decimal_places=2)
	units	=	models.IntegerField(default=1)
	amount	=	models.DecimalField(max_digits=12, decimal_places=2)

#---------------------------------------------------------
class RsvnBlog(models.Model) :
	rsvn	= 	models.ForeignKey(Rsvn,on_delete=models.CASCADE)
	clerk	= 	models.CharField(max_length=40)
	time	= 	models.DateTimeField(auto_now=True)
	desc	=	models.TextField()

#---------------------------------------------------------
