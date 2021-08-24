from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.contrib.auth.views  import logout_then_login

#from django.core.context_processors import csrf
#from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.db.models import Q
from collections import defaultdict
from django.utils.timezone import utc
from datetime import timedelta, date, time, datetime

import string
import calendar

from time import clock
from rsvn.models import *

#from rsvn.vctools.tools import *

colorList =( "White", "Burlywood","Red","Cyan","Blue","Green","Orange",
				"RoyalBlue","Orchid","NavajoWhite","Maroon","Sienna",
				"Yellow","Purple","DarkKhaki","Salmon","SeaGreen","OrangeRed","YellowGreen",
				"DarkCyan","Black","HotPink","Gray","Coral","SaddleBrown","SlateBlue")

#=====================================================================
def admin(request) :
#=====================================================================
	result ={}

	#=====================================

	return  render(request,'rsvn/admin.html',result )

#=====================================================================

@login_required
def index(request):
	result= {}
#	result.update (csrf(request))
	return render_to_response('rsvn/index.html',result )

#=====================================================================
def DateRangeSelect(request,span) :

	if  'view' not in request.POST :
		dateStart   = date.today().isoformat()
		dateEnd     = (date.today()+timedelta(days=span)).isoformat()

	if 'dateStart' in request.POST :
		dateStart = request.POST['dateStart']

	if 'dateEnd' in request.POST :
		dateEnd   = request.POST['dateEnd']

	return dateStart,dateEnd

#=====================================================================
@login_required
def current(request) :
	result = {}

	#--------------------------------------
	# Brc housekeeping grid
	#--------------------------------------
	brc = BRC()
	brc.user = request.user
#	brc.scan_checkout()

	if 'roomSelect' in request.POST :
		brc.clicker(request.POST['roomSelect'])

	if 'brcUpdate' in request.POST :
		brc.update_to_present()

	if 'brcReset' in request.POST :
		brc.currentReset()


	result['currentStatus'] = brc.roomGrid()

	
	return render(request,'revise/current.html',result)


#=====================================================================
@login_required
def available(request):
	result = {}

	# jquery tab check
	result.update(tab_state(request))

	#--------------------------------------
	# date span availability
	#--------------------------------------
	dateStart,dateEnd  = DateRangeSelect(request,18)
	avi = AvailabilityGrid(dateStart,dateEnd)
	result.update(avi.result)

	

	return render(request,'revise/available.html',result)

