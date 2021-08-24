from django.contrib import admin

from rsvn.models import *
# Register your models here.
#---------------------------------------------------------
class RateHeadingAdmin(admin.ModelAdmin) :
	list_display = ('title','descr',)
	ordering	 = ('title',)
#---------------------------------------------------------
class RateAtomAdmin(admin.ModelAdmin) :
	list_display 	= ('rateHeading','rateName','rateType','rateDays','lowSeason','highSeason','peakSeason',)
	ordering 		= ('rateName',)
#---------------------------------------------------------
class RoomInfoAdmin(admin.ModelAdmin) :
	list_display = ('type', 'number', 'beds','connect', 'notes')
	ordering = ('type','number')
#---------------------------------------------------------
class SeasonAdmin(admin.ModelAdmin) :
	list_display = ('name','beginDate','endDate')
	ordering = ('beginDate',)	

admin.site.register(RoomInfo,RoomInfoAdmin)

admin.site.register(Season,SeasonAdmin)

#admin.site.register(RateAtom,RateAtomAdmin)

#admin.site.register(RateHeading,RateHeadingAdmin)

#admin.site.register(ServiceRate,ServiceRateAdmin)

