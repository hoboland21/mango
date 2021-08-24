from datetime import time, date,timedelta

#-------------------------------------------------------------
# Grid matrix creates a convenient access to values and styles
# on a grid
#-------------------------------------------------------------
# available values are title,data,style,color,calcs

class gridMatrix(object):
	xLength = 0
	yLength = 0

	#-------------------------------------------------------------
	# x and y labels should be a list of 2 item list search name and title
	#-------------------------------------------------------------
	def loadY(self,yLabels):
	#-------------------------------------------------------------

		gridList = []

		self.xLength = len(self.seq)+1
		self.yLength = len(yLabels)+1
		self.gridList = [[{ 'title': "", 'data' : "" , 'style' : "", 'color' : "", 'calcs' : 0} for i in range(self.yLength)] for j in range(self.xLength)]
		self.xDict = {}
		self.yDict = {}
		#-------------------------------
		cntr = 1
		for label in self.seq :
			self.xDict[label[0]] = cntr
			self.gridList[cntr][0]['data'] = label[1]
			cntr += 1
		
		#-------------------------------
		cntr = 1
		for label in yLabels :
			self.yDict[label[0]] = cntr
			self.gridList[0][cntr]['data'] = label[1]
			cntr += 1
	


	#-------------------------------------------------------------
	def highlightRow(self,label) :
	#-------------------------------------------------------------
		row = self.yDict[label]
		for offset in range(self.xLength) :
			self.gridList[offset][row]['color'] = "silver"


	#-------------------------------------------------------------
	def highlightDate(self,date,color) :
	#-------------------------------------------------------------
		if date in self.xDict :
			x = self.xDict[date]
			self.gridList[x][0]['color'] = color	

	#-------------------------------------------------------------
	def dateSequenceX(self,startdate,**kwargs) :
	#-------------------------------------------------------------
		self.seq = []
		if 'days' in kwargs :
			for cnt in range(kwargs['days']) :
				thisDate = 	(startdate + timedelta(days=cnt)).date()
				self.seq.append([thisDate.isoformat(),thisDate])

		if 'format' in kwargs :
			for s in self.seq :
				s[1] = date.strftime(s[1],kwargs['format'])


	#-------------------------------------------------------------
	def coord(self,xLabel,yLabel):
	#-------------------------------------------------------------
	# enter x label and y label values and get back an x,y pair
	#-------------------------------------------------------------

		x = self.xDict[xLabel]
		y = self.yDict[yLabel]
		return [x,y]

	#-------------------------------------------------------------
	def put(self,name,xLabel,yLabel,data) :
	#-------------------------------------------------------------
	# name of cell and xlabel and ylabel will put data
	#-------------------------------------------------------------
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y][name] = data


	#-------------------------------------------------------------
	def get(self,name,xLabel,yLabel):
	#-------------------------------------------------------------
	# name of cell and xlabel and ylabel will get data
	#-------------------------------------------------------------
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y][name]

	#-------------------------------------------------------------
	def HTML(self):
	#-------------------------------------------------------------
		html = ""
		for y in range(self.yLength) :
			html += "<tr class='g_row' id='rownum{}'>".format(y)
			for x in range(self.xLength) :
				data = self.gridList[x][y]['data']
				style = self.gridList[x][y]['style']
				color = self.gridList[x][y]['color']
				title = self.gridList[x][y]['title']
				if x==0 :
					last = "<th class='y_label_class' title='{3}'  style=background-color:{0}; {1}'>{2}</th>".format(color,style,data,title)
					html +=  last

				elif  y==0 :
					html += "<th class='x_label_class' title='{3}'  style=background-color:{0}; {1}'>{2}</th>".format(color,style,data,title)
				else :
					html += "<td title='{3}' style='background-color:{0};  {1}'>{2}</td>".format(color,style,data,title)

			html += "{} </tr>".format(last)
		return html

#-------------------------------------------------------------
# Grid matrix creates a convenient access to values and styles
# on a grid
#-------------------------------------------------------------
# available values are title,data,style,color,calcs

class tableMatrix(object):
	xLength = 0
	yLength = 0
	xLabels =[]
	yLabels = []

	#-------------------------------------------------------------
	# x and y labels should be a list of 2 item list search name and title
	#-------------------------------------------------------------
	def loadTable(self):
	#-------------------------------------------------------------

		self.xLength = len(self.xLabels)+1
		self.yLength = len(self.yLabels)+1
		self.gridList = [[{ 'title': "", 'data' : "" , 'style' : "", 'color' : "", 'calcs' : 0} for i in range(self.yLength)] for j in range(self.xLength)]
		self.xDict = {}
		self.yDict = {}
		
		#-------------------------------
		cntr = 1
		for label in self.xLabels :
			self.xDict[label[0]] = cntr
			self.gridList[cntr][0]['data'] = label[1]
			cntr += 1
		
		#-------------------------------
		cntr = 1
		for label in self.yLabels :
			self.yDict[label[0]] = cntr
			self.gridList[0][cntr]['data'] = label[1]
			cntr += 1
	#-------------------------------------------------------------
	def dateSequence(self,startdate,**kwargs) :
	#-------------------------------------------------------------
		self.seq = []
		if 'days' in kwargs :
			for cnt in range(kwargs['days']) :
				thisDate = 	(startdate + timedelta(days=cnt)).date()
				self.seq.append([thisDate.isoformat(),thisDate])

		if 'format' in kwargs :
			for s in self.seq :
				s[1] = date.strftime(s[1],kwargs['format'])

		if 'axis' in kwargs :
			if kwargs['axis'] == 'x' :
				self.xLabels = self.seq
			if  kwargs['axis'] == 'y' :
				self.yLabels = self.seq

#-------------------------------------------------------------
	def highlightRow(self,label) :
	#-------------------------------------------------------------
		row = self.yDict[label]
		for offset in range(self.xLength) :
			self.gridList[offset][row]['color'] = "silver"


	#-------------------------------------------------------------
	def highlightDate(self,date,color) :
	#-------------------------------------------------------------
		if date in self.yDict :
			y = self.yDict[date]
			self.gridList[0][y]['color'] = color	


	#-------------------------------------------------------------
	def coord(self,xLabel,yLabel):
	#-------------------------------------------------------------
	# enter x label and y label values and get back an x,y pair
	#-------------------------------------------------------------

		x = self.xDict[xLabel]
		y = self.yDict[yLabel]
		return [x,y]

	#-------------------------------------------------------------
	def put(self,name,xLabel,yLabel,data) :
	#-------------------------------------------------------------
	# name of cell and xlabel and ylabel will put data
	#-------------------------------------------------------------
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y][name] = data


	#-------------------------------------------------------------
	def get(self,name,xLabel,yLabel):
	#-------------------------------------------------------------
	# name of cell and xlabel and ylabel will get data
	#-------------------------------------------------------------
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y][name]

	#-------------------------------------------------------------
	def HTML(self):
	#-------------------------------------------------------------
		html = ""
		for y in range(self.yLength) :
			html += "<tr>"
			for x in range(self.xLength) :
				data = self.gridList[x][y]['data']
				style = self.gridList[x][y]['style']
				color = self.gridList[x][y]['color']
				title = self.gridList[x][y]['title']
				if x==0 :
					html += "<th class='y_label_class' title='{3}'  style=background-color:{0}; {1}'>{2}</th>".format(color,style,data,title)
				elif  y==0 :
					html += "<th class='x_label_class' title='{3}'  style=background-color:{0}; {1}'>{2}</th>".format(color,style,data,title)
				else :
					html += "<td title='{3}' style='background-color:{0};  {1}'>{2}</td>".format(color,style,data,title)

			html += "</tr>"
		return html

#-------------------------------------------------------------
