
TYPE_NAME_DICT = {
	'standard' :'Standard',	'deluxe': 'Deluxe',
	'pool_deluxe' :'Pool Deluxe',	'lanai' : 'Lanai',
	'presidential' : 'Presidential',	'manor' : 'Manor',
	'suites':'Suites','garden':'Garden'
	}

SORT_ORDER_LIST =  [ 	'standard','deluxe','pool_deluxe','lanai','presidential','manor','suites','garden']

VACANT 		= 0
OCCUPIED 	= 1
DIRTY 		= 2
CLEAN_SCHED = 3
OOC			= 4
BB			= 5

NO_CANCEL 	= 	True
REVERSE 	=	False

INCLUDE_CANCEL = 0
EXCLUDE_CANCEL = 1

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
	('White','White'), 
	('Burlywood','Burlywood'),
	('Red','Red'),
	('Cyan','Cyan'),
	('Blue','Blue'),
	('Green','Green'),
	('Orange','Orange'),
	('RoyalBlue','RoyalBlue'),
	('Orchid','Orchid'),
	('NavajoWhite','NavajoWhite'),
	('Maroon','Maroon'),
	('Sienna','Sienna'),
	('Yellow','Yellow'),
	('Purple','Purple'),
	('DarkKhaki','DarkKhaki'),
	('Salmon','Salmon'),
	('SeaGreen','SeaGreen'),
	('OrangeRed','OrangeRed'),
	('YellowGreen','YellowGreen'),
	('DarkCyan','DarkCyan'),
	('Black','Black'),
	('HotPink','HotPink'),
	('Gray','Gray'),
	('Coral','Coral'),
	('SaddleBrown','SaddleBrown'),
	('SlateBlue','SlateBlue')
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
roomStateDict = { 0:'CLEAN',1:'OCCUPIED',2:'DIRTY',3:'SCHED',4:'OOC',5:'BB',6:'ATTN'}
roomStateDictReverse = {'CLEAN':0,'OCCUPIED':1,'DIRTY':2,'SCHED':3,'OOC':4,'BB':5,'ATTN':6}

