from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Form, Textarea, TextInput, HiddenInput
from django import forms
from datetime import *
from decimal import Decimal



#---------------------------------------------------------
ROOM_CURRENT = (
	('repair', 'Repair'),
	('occupied', 'Occupied'),
	('clean','Clean'),
	('dirty','Dirty')
)

#---------------------------------------------------------
COLOR_CHOICES = {
	"white" : 0xFFFF,
	"black" : 0x0000,
	}

#---------------------------------------------------------
COLORLIST =(
	("White","White"), 
	("Burlywood","Burlywood"),
	("Red","Red"),
	("Cyan","Cyan"),
	("Blue","Blue"),
	("Green","Green"),
	("Orange","Orange"),
	("RoyalBlue","RoyalBlue"),
	("Orchid","Orchid"),
	("NavajoWhite","NavajoWhite"),
	("Maroon","Maroon"),
	("Sienna","Sienna"),
	("Yellow","Yellow"),
	("Purple","Purple"),
	("DarkKhaki","DarkKhaki"),
	("Salmon","Salmon"),
	("SeaGreen","SeaGreen"),
	("OrangeRed","OrangeRed"),
	("YellowGreen","YellowGreen"),
	("DarkCyan","DarkCyan"),
	("Black","Black"),
	("HotPink","HotPink"),
	("Gray","Gray"),
	("Coral","Coral"),
	("SaddleBrown","SaddleBrown"),
	("SlateBlue","SlateBlue")
	)

#---------------------------------------------------------
ROOM_TYPE_CHOICES = (
   ('standard','Standard'),
   ('deluxe','Deluxe'),
   ('pool_deluxe','Pool Deluxe'),
   ('lanai','Lanai'),
   ('presidential','Presidential'),
   ('manor','Manor'),
   ('suites','Suites'),
   ('garden','Garden'),
   )#---------------------------------------------------------
RATE_TYPE_CHOICES = (
   ('standard','Standard'),
   ('deluxe','Deluxe'),
   ('pool_deluxe','Pool Deluxe'),
   ('lanai','Lanai'),
   ('presidential','Presidential'),
   ('manor','Manor'),
   ('SERVICE','SERVICE'),
   ('suites','Suites'),
   ('garden','Garden'),
   )


#---------------------------------------------------------
SOURCE_CHOICES = (
	('local_fit','Local FIT'),
	('tour','Tour Agency'),
	('fit','Tour FIT'),
	('govt','Government'),
	('promo','Promotional'),
	('rack','Rack Rate'),
)

#---------------------------------------------------------
RESERVATION_STATUS = (
	('notconfirmed','Not Confirmed'),
	('confirmed','Confirmed'),
	('checkin','Checking In'),
	('checkout','Checking Out'),
	('notpaid','Not Paid'),
	('prepaid' ,'Prepaid'),
	('cancel','Cancel'),
	('noshow', 'No Show'),
)

#---------------------------------------------------------
ROOM_STATUS = (
	('checkin','Check In'),
	('checkout','Check Out'),
	('clean','Clean'),
	('dirty','Dirty'),
	('working','Working'),
	('none','None'),

)

#---------------------------------------------------------
VENUE_CHOICES = (
	('pool','Swimming Pool'),
	('confroom2','Conference 2nd'),
	('confroom3','Conference 3rd'),
	('cafe' ,'Cafe'),
	('vcourt','Volleyball Court'),
	('lobby','Lobby'),
	('back','Back Space'),	
	('other','Other'),
) 


#---------------------------------------------------------
TRANSACTION_TYPE = (
   ('charge','Charge'),
   ('discount','Discount'),
   ('tax','Tax'),
   ('payment', 'Payment'),
   ('room','Room Charge'),
   ('refund','Refund'),
   )

#---------------------------------------------------------
SEASON_LEVEL = (
	('high','High Season'),
	('low','Low Season'),
	('peak','Peak Season'),
	)

REQUIRED_FIELDS = ('adult','rooms','type','dateOut','beds','dateIn','status','firstname',
				   'lastname','source','phone1','country','agent')
#---------------------------------------------------------

SERVICE_FIELDS = { 
	'from_airport'	: 'From Airport Trans',
	'to_airport'	: 'To Airport Trans',
	'earlyin'		: 'Early Check In',
	'lateout' 		: 'Late Check Out',
	'connect' 		: 'Connecting Room',
	'dailymaid'		: 'Daily Maid Service',
	'extrabed'		: 'Extra Bed',
	'mango' 		: 'Mango Access',
	'breakfast'		: 'Breakfast',
	'lunch'			: 'Lunch',
	'dinner'		: 'Dinner',
	'crib'			: 'Baby Crib',
	'event'			: 'Event'
	}
#---------------------------------------------------------

SERVICE_FIELDS_ABV = { 
	'from_airport'	: 'FrmA',
	'to_airport'	: 'ToA',
	'breakfast'		: 'Brkf',
	'lunch'			: 'Lnch',
	'dinner'		: 'Dinr',
	'earlyin'		: 'EIn',
	'lateout' 		: 'LOut',
	'connect' 		: 'Conn',
	'dailymaid'		: 'DMd',
	'extrabed'		: 'Bed',
	'mango' 		: 'MAcc',
	'crib'			: 'Crib',
	'event'			: 'Event'
	  }
	  
#---------------------------------------------------------
 

RC1List = ('status','firstname','lastname', 'source','rate','phone1', 'phone2','city','country','email')
RC2List = ('dateIn','dateOut', 'type','rooms','beds','adult','child','infant','notes')

#---------------------------------------------------------


RATEHEADING_DEFAULT_DICT = {
	'local_fit':'Local FIT',
	'tour':'Tour Agency',
	'fit':'Tour FIT',
	'govt':'Government',
	'promo':'Promotional',
	'rack':'Rack Rate',
	'SERVICE':'SERVICE'
	}
	
	
ROOM_TYPE_DICT_REV = {
   'Standard':'standard',
   'Deluxe':'deluxe',
   'Pool Deluxe':'pool_deluxe',
   'Lanai':'lanai',
   'Presidential':'presidential'
   
   }
	
	
ROOM_TYPE_DICT = {
   'standard':'Standard',
   'deluxe':'Deluxe',
   'pool_deluxe':'Pool Deluxe',
   'lanai':'Lanai',
   'presidential':'Presidential'
   
   }

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
		
#---------------------------------------------------------
class Rsvn (models.Model):
	status		=	 models.CharField(max_length=13, choices=RESERVATION_STATUS)

	firstname	=	models.CharField(max_length=30)
	lastname 	=	models.CharField(max_length=30)

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

	notes		=	models.TextField(blank=True)

	city 		= 	models.CharField(max_length=30,blank=True)
	country 	= 	models.CharField(max_length=30)

	email 		= 	models.EmailField(blank=True)


	confirm		=   models.CharField(max_length=20, blank=True)
	clerk		=   models.CharField(max_length=20, blank=True)

	def num_days (self):
		return  (self.dateOut - self.dateIn).days

	def __str__(self):
		fullname = "%s %s  %s - %s" % (self.firstname, self.lastname,self.dateIn, self.dateOut )
		return(fullname)

#--------------------------------------------------------------------
class RsvnForm(ModelForm):
	class Meta:
		model= Rsvn
		exclude = ['confirm','clerk']
		labels = { 'dateIn': 'Check In', 'dateOut' : 'Check Out'}
		widgets = {
			'dateIn'	:TextInput 	(attrs={'class':'datepicker'}),
			'dateOut'  :TextInput 	(attrs={'class':'datepicker'}),
			'notes'		:Textarea	(attrs={'cols': 20, 'rows': 2}),
			}

#--------------------------------------------------------------------
class RateHeading(models.Model) :
	title		=	models.CharField(max_length=256)
	descr		=	models.CharField(max_length=1028)

	def __str__(self):
		return(self.title)		

#---------------------------------------------------------
class RateHeadingForm(ModelForm) :
	class Meta :
		model = RateHeading
		fields = '__all__'
		
#---------------------------------------------------------
class RateHeadingAdmin(admin.ModelAdmin) :
	list_display = ('title','descr',)
	ordering	 = ('title',)


#---------------------------------------------------------
class RateAtom(models.Model):
	rateheading =   models.ForeignKey(RateHeading)
	rateName	=	models.CharField(max_length=512, blank=True)
	rateType	=  	models.CharField(max_length=128, choices=RATE_TYPE_CHOICES)
	lowSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	highSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	peakSeason	= 	models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('00.00'))
	
	def __str__(self):
		return(self.rateName)
#---------------------------------------------------------
class RateAtomForm(ModelForm) :
	class Meta :
		model = RateAtom
		exclude  = ['rateheading']

#---------------------------------------------------------
class RateAtomAdmin(admin.ModelAdmin) :
	list_display 	= ('rateHeading','rateName','rateType','rateDays','lowSeason','highSeason','peakSeason',)
	ordering 		= ('rateName',)

#--------------------------------------------------------------------
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
class AgentForm(ModelForm) :
	class Meta:
		fields = '__all__'
		model= Agent

#--------------------------------------------------------------------
class AgentRate(models.Model) :
	agent 			= 	models.ForeignKey(Agent)
	rateheading		=	models.ForeignKey(RateHeading)



#--------------------------------------------------------------------
class Service (models.Model):
	rsvn			= 	models.ForeignKey(Rsvn)
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


#=========================================================
class Tour (models.Model):
	agent			= 	models.ForeignKey(Agent)
	rsvn			= 	models.ForeignKey(Rsvn)
	arrive_flight	= 	models.CharField(max_length=30, blank=True)
	arrive_time		=	models.DateTimeField()
	depart_flight	= 	models.CharField(max_length=30, blank=True)
	depart_time		=	models.DateTimeField()
	promo			=	models.TextField(blank=True)

	def __str__(self) :
		return "{} - {}".format(self.agent.agency, self.arrive_time)

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


#=========================================================
class Scheme (models.Model):
	rsvn		= 	models.ForeignKey(Rsvn)
	gridColor 	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	rsvnColor   = 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	extraColor	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	def __str__(self):
		gC = "{} - {}  {}  {}".format(self.rsvn.firstname, self.gridColor, self.rsvnColor, self.extraColor )
		return(gC)

#--------------------------------------------------------------------
class SchemeForm(ModelForm) :
	class Meta:
		model= Scheme
		fields = '__all__'
		exclude = ['rsvn','rsvnColor','extraColor']


#=========================================================
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
#---------------------------------------------------------
class RoomInfoAdmin(admin.ModelAdmin) :
	list_display = ('type', 'number', 'beds','connect', 'notes')
	ordering = ('type','number')

#---------------------------------------------------------
class Room (models.Model):
	rsvn		=    models.ForeignKey(Rsvn)
	roominfo 	=	 models.ForeignKey(RoomInfo)
	info		=  	 models.CharField(max_length=512, blank=True)
	roomstatus	=	 models.CharField(max_length=13, choices=ROOM_STATUS,blank=True)

	
	def __str__(self):
		fullname = "%s %s" % (self.rsvn,self.roominfo )
		return(fullname)

#---------------------------------------------------------
class RoomForm(ModelForm) :
	class Meta:
		fields = '__all__'
		model= Room

#---------------------------------------------------------
class Event(models.Model) :
	rsvn		= models.ForeignKey(Rsvn)
	title		= models.CharField(max_length=128)
	pax			= models.IntegerField(validators = [ MinValueValidator(1) ])
	descr		= models.TextField()
	venue 		= models.CharField(max_length=90,choices=VENUE_CHOICES)
	dateStart	= models.DateField( )
	timeStart	= models.TimeField( default = "00:00:00")
	dateEnd		= models.DateField( )
	timeEnd		= models.TimeField( default = "00:00:00")

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
class Season(models.Model) :
	name		=	models.CharField(max_length=140)
	season		= 	models.CharField(max_length=40, choices=SEASON_LEVEL )
	beginDate	=	models.DateField()
	endDate		=	models.DateField()
	def __str__(self):
		return(self.name)

#---------------------------------------------------------
class SeasonAdmin(admin.ModelAdmin) :
	list_display = ('name','beginDate','endDate')
	ordering = ('beginDate',)	

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
class CurrentLog(models.Model) :
	date		= models.DateField(unique=True)
	log			= models.TextField()

#---------------------------------------------------------
class Invoice(models.Model) :
	rsvn			= 	models.ForeignKey(Rsvn)
	rateheading 	=	models.ForeignKey(RateHeading)
	rateName		=	models.CharField(max_length=512)
	number			=	models.CharField(max_length=100)
	date_created	=	models.DateField(auto_now=True)
	date_sent		= 	models.DateField(default=date(2010,1,1) )
	date_paid		=	models.DateField(default=date(2010,1,1) )
	text_record		=	models.TextField(blank=True)

#---------------------------------------------------------
class InvoiceEntry(models.Model) :
	invoice	= 	models.ForeignKey(Invoice)
	clerk	= 	models.CharField(max_length=40)
	time	= 	models.DateTimeField(auto_now=True)
	type   	= 	models.CharField(max_length=64)
	desc	=	models.CharField(max_length=256)
	cost	=	models.DecimalField(max_digits=12, decimal_places=2)
	units	=	models.IntegerField(default=1)
	amount	=	models.DecimalField(max_digits=12, decimal_places=2)

#---------------------------------------------------------
class InvoiceEntryForm(ModelForm) :
	class Meta :
		model = InvoiceEntry
		exclude = ['time','clerk']
	
#---------------------------------------------------------
class RsvnBlog(models.Model) :
	rsvn	= 	models.ForeignKey(Rsvn)
	clerk	= 	models.CharField(max_length=40)
	time	= 	models.DateTimeField(auto_now=True)
	desc	=	models.TextField()

#---------------------------------------------------------
class RsvnBlogForm(ModelForm) :
	class Meta:
		model= RsvnBlog
		exclude = ['rsvn','clerk','time']
		widgets = {
			'desc' :Textarea	(attrs={'cols': 25, 'rows': 2}),
			}
