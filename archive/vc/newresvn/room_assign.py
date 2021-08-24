
		# adding a room is selected
		if self.arg_check("roomSelect") :
			roomNumber = self.args_put['roomSelect']
			if rs1.room_ok(roomNumber) and len(Room.objects.filter(rsvn__id__exact=self.rsvnid)) < self.rsvn.rooms:
				roominfo = RoomInfo.objects.get(number__exact = roomNumber)
				room  = Room(rsvn=self.rsvn,roominfo=roominfo,roomstatus='none')
				room.save()
				rs1.change_room(roomNumber,"mine")

		# deleting a room is selected
		if self.arg_check("delRoom") :
			roomNumber = self.args_put['delRoom']
			rs1.change_room(roomNumber,"")
			rmchk =	Room.objects.get(roominfo__number = roomNumber,rsvn_id = self.rsvn.id)
			rmchk.delete()


	
	#----------------------------------
	def roomToggles(self) :
	#----------------------------------
		#pressing roomInStatus 
		if self.arg_check("roomInSelect") :
			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomInSelect"])
			room.roomstatus = "checkin"
			room.save()
		#pressing roomOutStatus 
		if self.arg_check("roomOutSelect") :
			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomOutSelect"])
			room.roomstatus = "checkout"
			room.save()

		#pressing roomNoneStatus 
#		if self.arg_check("roomNoneSelect") :
#			room = Room.objects.get(rsvn__id=self.rsvnid,roominfo__number=self.args_put["roomNoneSelect"])
#			room.roomstatus = "none"
#			room.save()
		#==========================
		# we check for a global button push
		check = ""
		#pressing globalIn 
		if self.arg_check("globalIn") :
			check ="checkin" 
		#pressing globalOut 
		if self.arg_check("globalOut") :
			check="checkout"
		#pressing globalNone 
#		if self.arg_check("globalNone") :
#			check="none"

		if check != "" :
			for room in Room.objects.filter(rsvn__id=self.rsvnid) :
				room.roomstatus = check
				room.save()