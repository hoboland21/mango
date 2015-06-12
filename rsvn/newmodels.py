from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Form, Textarea, TextInput, HiddenInput
from django import forms
from datetime import *
#================================
ROOM_CURRENT = (
	('repair', 'Repair'),
	('occupied', 'Occupied'),
	('clean','Clean'),
	('dirty','Dirty')
)

COLOR_CHOICES = {
	"white" : 0xFFFF,
	"black" : 0x0000,

				}


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

ROOM_TYPE_CHOICES = (
   ('standard','Standard'),
   ('deluxe','Deluxe'),
   ('pool_deluxe','Pool Deluxe'),
   ('lanai','Lanai'),
   ('presidential','Presidential'),
   ('manor','Manor'),
   ('suites','Suites')
   )


SOURCE_CHOICES = {
	('local_fit','Local FIT'),
	('tour','Tour Agency'),
	('fit','Tour FIT'),

	('govt','Government'),
	('promo','Promotional'),
	('rock','Rack Rate'),
}

RESERVATION_STATUS = (
	('notconfirmed','Not Confirmed'),
	('confirmed','Confirmed'),
	('checkin','Checked In'),
	('checkout','Checked Out'),
	('notpaid','Not Paid'),
	('prepaid' ,'Prepaid'),
	('cancel','Cancel'),
	('noshow', 'No Show'),
)
ROOM_STATUS = (
	('checkin','Checked In'),
	('checkout','Checked Out'),
	('clean','Clean'),
	('dirty','Dirty'),
	('working','Working'),
	('none','None'),


)
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


#--------------------------------------------------------------------
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

	credit 		= 	models.CharField(max_length=30, blank=True )
	creditexp 	= 	models.CharField(max_length=8, blank=True )
	creditcvv	= 	models.CharField(max_length=5, blank=True )

	confirm		=   models.CharField(max_length=20, blank=True)
	clerk		=   models.CharField(max_length=20, blank=True)

	def num_days (self):
		return  (self.dateOut - self.dateIn).days

	def __unicode__(self):
		fullname = "%s %s  %s - %s" % (self.firstname, self.lastname,self.dateIn, self.dateOut )
		return(fullname)

#--------------------------------------------------------------------
class RsvnForm(ModelForm):
	class Meta:
		model= Rsvn
		fields = '__all__'
		
		exclude = ['confirm','clerk']
		labels = { 'dateIn': 'Check In', 'dateOut' : 'Check Out'}
		widgets = {

			'dateIn'	:TextInput 	(attrs={'class':'datepicker'}),
			'dateOut'  :TextInput 	(attrs={'class':'datepicker'}),
			'notes'		:Textarea	(attrs={'cols': 20, 'rows': 2}),
			}
#--------------------------------------------------------------------
class RsvnContactForm(ModelForm):
	class Meta:
		model= Rsvn
		fields = ('status','firstname','lastname', 'source','phone1', 'phone2','city','country','email')

#--------------------------------------------------------------------

class RsvnCheckForm(ModelForm):
	class Meta:
		model= Rsvn
		fields = ('dateIn','dateOut', 'type','rooms','beds','adult','child','infant','notes')



		labels = { 'dateIn': 'Check In', 'dateOut' : 'Check Out'}
		widgets = {
			'dateIn'	:TextInput 	(attrs={'class':'datepicker'}),
			'dateOut'  :TextInput 	(attrs={'class':'datepicker'}),
			'notes'		:Textarea	(attrs={'cols': 20, 'rows': 2}),
			}
#--------------------------------------------------------------------
class Agent (models.Model):
	agency			=	models.CharField(max_length=30)
	contact			= 	models.CharField(max_length=30, blank=True)
	telephone		= 	models.CharField(max_length=20, blank=True)
	fax				= 	models.CharField(max_length=20, blank=True)
	email 			= 	models.EmailField(blank=True)
	notes			=	models.TextField(blank=True)

	def __unicode__(self):
		return self.agency
#--------------------------------------------------------------------
class AgentForm(ModelForm) :
	class Meta:
		model= Agent
#=========================================================
class Service (models.Model):
	rsvn			= 	models.ForeignKey(Rsvn)
	breakfast		=	models.BooleanField(default=False)
	airport			=	models.BooleanField(default=False)
	dailymaid		=	models.BooleanField(default=False)
	extrabed		=	models.BooleanField(default=False)
	crib			=	models.BooleanField(default=False)
	connect			=	models.BooleanField(default=False)
	earlyin			=	models.BooleanField(default=False)
	lateout			=	models.BooleanField(default=False)
	
#--------------------------------------------------------------------
class ServiceForm(ModelForm) :
	class Meta:
		model= Service

		fields= '__all__'
		labels = { 'airport': 'Airport Trans',
				  'earlyin' : 'Early Check In',
				  'lateout' : 'Late Check Out',
				  'connect' : 'Connecting Room',
				  'dailymaid': 'Daily Maid Service',
				  'extrabed': 'Extra Bed'}

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

	def __unicode__(self) :
		return " {} - {}".format(self.agent,self.arrive_time)
#--------------------------------------------------------------------
class TourForm(ModelForm) :
	class Meta:
		model= Tour
		fields = '__all__'
		exclude = ['rsvn']
		widgets = {
			'arrive_time' :TextInput  (attrs={'class':'datetimepicker'}),
			'depart_time' :TextInput  (attrs={'class':'datetimepicker'}),
			'promo' :Textarea	(attrs={'cols': 20, 'rows': 2}),
			}
#=========================================================
class Scheme (models.Model):
	rsvn		= 	models.ForeignKey(Rsvn)
	gridColor 	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	rsvnColor   = 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	extraColor	= 	models.CharField(max_length=15,choices=COLORLIST,default='white')
	def __unicode__(self):
		gC = "{} - {}  {}  {}".format(self.rsvn.firstname, self.gridColor, self.rsvnColor, self.extraColor )
		return(gC)
#--------------------------------------------------------------------
class SchemeForm(ModelForm) :
	class Meta:
		model= Scheme
		fields = '__all__'
		exclude = ['rsvn']

#=========================================================
class RoomInfo (models.Model):
	number		=	models.CharField(max_length=5)
	type		=	models.CharField(max_length=25, choices=ROOM_TYPE_CHOICES)
	beds		=	models.IntegerField(default=1,validators = [ MinValueValidator(1) ])
	connect	 	=   models.CharField(max_length=5, blank=True)
	notes		=	models.TextField(blank=True)
	current		=	models.IntegerField(default=0)

	def __unicode__(self):
		fullname = "Room %s - %s - %s Beds" % (self.number, self.type,self.beds )
		return(fullname)
#---------------------------------------------------------
class RoomInfoAdmin(admin.ModelAdmin) :
	list_display = ('type', 'number', 'beds','connect', 'notes')
	ordering = ('type','number')

#=========================================================
class Room (models.Model):
	rsvn		=    models.ForeignKey(Rsvn)
	roominfo 	=	 models.ForeignKey(RoomInfo)
	info		=  	 models.CharField(max_length=512, blank=True)
	roomstatus	=	 models.CharField(max_length=13, choices=ROOM_STATUS,blank=True)

	def __unicode__(self):
		fullname = "%s %s" % (self.rsvn,self.roominfo )
		return(fullname)
#---------------------------------------------------------
class RoomForm(ModelForm) :
	class Meta:
		model= Room
#=========================================================
class EventCalendar(models.Model) :

	title		= models.CharField(max_length=128)
	pax			= models.IntegerField(validators = [ MinValueValidator(1) ])
	event		= models.TextField(blank=True)
	date		= models.DateField(default=datetime.now().date().isoformat() )
	clerk		= models.CharField(max_length=40)
	confirm		= models.CharField(max_length=20, blank=True)
#=========================================================
class Event(models.Model) :

	title		= models.CharField(max_length=128)
	pax			= models.IntegerField(validators = [ MinValueValidator(1) ])
	descr		= models.TextField(blank=True)
	venue 		= models.CharField(max_length=90,choices=VENUE_CHOICES)
	dateStart	= models.DateTimeField( )
	dateEnd 	= models.DateTimeField( )
	clerk		= models.CharField(max_length=40)

#---------------------------------------------------------
class EventForm(ModelForm) :
	class Meta:
		model= Event
		exclude = ['clerk','confirm']
		widgets = {
			'event'		:Textarea	(attrs={'cols': 30, 'rows': 10, 'class' : 'leftjust' }),
			'dateStart'		:TextInput 	(attrs={'class':'datetimepicker'}),
			'dateEnd'		:TextInput 	(attrs={'class':'datetimepicker'}),

			}

#---------------------------------------------------------
class Chat(models.Model) :
	clerk		= models.CharField(max_length=40)
	time		= models.DateTimeField( )
	title		= models.CharField(max_length=128)
	subject		= models.CharField(max_length=256)
	item		= models.TextField()
#---------------------------------------------------------
class ChatForm(ModelForm) :
	class Meta :
		model = Chat
		exclude = ['date']

#---------------------------------------------------------






