from django.contrib import admin

from rsvn.models import *
# Register your models here.

admin.site.register(RoomInfo,RoomInfoAdmin)

admin.site.register(Season,SeasonAdmin)

#admin.site.register(RateAtom,RateAtomAdmin)

#admin.site.register(RateHeading,RateHeadingAdmin)

#admin.site.register(ServiceRate,ServiceRateAdmin)

