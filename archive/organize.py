def detail(request,rsvnid) :
	if 'rsvnNew' in request.POST :
		return redirect('entry')
	# in case our reservation hs been changed, we need to
	# flush our context 
	if 'rsvnid' in request.POST :
		if request.POST['rsvnid'] != rsvnid :
			return redirect('detail',request.POST['rsvnid'])
	
	result = {}

	# ==================================================
	# This is to keep the tabs in place after selected
	# ==================================================
	result["mode"] = 0
	result["mode2"] = 1

	if 'mode' in request.POST :
		print "Mode -",request.POST['mode']
		result['mode'] = request.POST['mode']
	if 'mode2' in request.POST :
		print "Mode2 -",request.POST['mode2']
		result['mode2'] = request.POST['mode2']
	# ==================================================

	rvn = RsvnControl()
	rvn.load(rsvnid)
	rvn.existingForm()

	roomCtrl = RsvnRoomControl(rvn.rsvn)
	
	#=====================================
	# Tour info saved
	#=====================================	
	if 'tourSave' in request.POST :
		rvn.saveTour(request)
	
	#=====================================
	# Rooms added or deleted here for regular
	#=====================================
	if 'roomSelect' in request.POST : 
		number = request.POST['roomSelect']
		roomCtrl.addRoom(number)

	if 'delRoom' in request.POST  : 
		number = request.POST['delRoom']
		roomCtrl.delRoom(number)
	
	b2b = B2B(rvn.rsvn.id)
	

	#=====================================
	# Rooms added or deleted here for b2b
	#=====================================
	if 'roomSelectB2B' in request.POST : 
		number = request.POST['roomSelectB2B']
		b2b.addRoom(number)

	if 'delRoomB2B' in request.POST  : 
		number = request.POST['delRoomB2B']
		b2b.delRoom(number)
	#=====================================
	# Save any changes made to the current record
	#=====================================
	if  'rsvnSave' in request.POST :
		if 'gridColor' in request.POST :
			rvn.gridColor = request.POST['gridColor']
		rvn.save(request)


	# The delete function has to be checked
	######################################## 
	if 'rsvnDelete' in request.POST:
		rsvnidSelect = request.POST['rsvnDelete'] 
		result['rsvnidSelect'] = rsvnidSelect
		result['rsvnDelete'] = True

	
	if 'verify' in request.POST :
		if request.POST['verify'] == "delete" :
			rvn.load(request.POST['rsvnidSelect'])
			rvn.delete()
	#=====================================


	#=====================================
	# Reservation List Selector
	#=====================================
	result['viewSelect'] = 'center'	
	if 'viewSelect' in request.POST :
		result['viewSelect'] = request.POST['viewSelect']	

	#=====================================
		
	#--- preparing rsvn_list
	result['rsvn_list'] = rsvnListMake()
		
	#--- preparing room list
	roomList = Room.objects.filter(rsvn_id__exact=rvn.rsvnid)
	

	# -- Refresh Room Control
	roomCtrl = RsvnRoomControl(rvn.rsvn)

	result['roomProfile'] = roomProfileMake()

	result.update(rvn.result())	
	result['colorList'] = colorList
	result['roomGrid']      	= roomCtrl.roomGrid()
	result['roomGridB2B']      	= b2b.roomGrid()
	result['assignedRooms']  	= len(roomList)
	result['roomList']      	= roomList
	result['location'] 	= 'entry'
	result.update (csrf(request))
	
	return render('rsvn/entry.html',result )
