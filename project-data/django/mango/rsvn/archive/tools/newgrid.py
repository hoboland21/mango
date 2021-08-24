#-------------------------------------------------------------
class GridMatrix(object):
	gridList = []
	xDict = {}
	yDict = {}
	xLength = 0
	yLength = 0

#-------------------------------------------------------------
	def __init__ (self,xLabels,yLabels):
		self.xLength = len(xLabels)
		self.yLength = len(yLabels)

		self.gridList = [[{ 'title': "", 'data' : "" , 'style' : "", 'color' : "", 'calcs' : 0} for i in range(self.yLength)] for j in range(self.xLength)]
		self.xDict = {}
		self.yDict = {}

		cntr = 0
		for label in xLabels :
			self.xDict[label] = cntr
			self.gridList[cntr][0]['data'] = label
			cntr += 1
		cntr = 0
		for label in yLabels :
			self.yDict[label] = cntr
			self.gridList[0][cntr]['data'] = label
			cntr += 1

#-------------------------------------------------------------
	def coord(self,xLabel,yLabel):
		x = self.xDict[xLabel]
		y = self.yDict[yLabel]
		return [x,y]

#-------------------------------------------------------------
	def put(self,name,xLabel,yLabel,data) :
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y][name] = data
#-------------------------------------------------------------
	def get(self,name,xLabel,yLabel):
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y][name]


#-------------------------------------------------------------
	def putData(self,xLabel,yLabel,data):
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y]['data'] = data
#-------------------------------------------------------------
	def getData(self,xLabel,yLabel):
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y]['data']


#-------------------------------------------------------------
	def putXData(self,xLabel,data):
		x = self.xDict[xLabel]
		self.gridList[x][0]['data'] = data
#-------------------------------------------------------------
	def getXData(self,xLabel):
		x = self.xDict[xLabel]
		return self.gridList[x][0]['data']


#-------------------------------------------------------------
	def putYData(self,yLabel,data):
		y = self.yDict[yLabel]
		self.gridList[0][y]['data'] = data
#-------------------------------------------------------------
	def getYData(self,yLabel):
		y = self.yDict[yLabel]
		return self.gridList[0][y]['data']



#-------------------------------------------------------------
	def putStyle(self,xLabel,yLabel,style):
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y]['style'] = style
#-------------------------------------------------------------
	def getStyle(self,xLabel,yLabel):
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y]['style']


#-------------------------------------t-----------------------
	def putColor(self,xLabel,yLabel,color):
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y]['color'] = color
#-------------------------------------------------------------
	def getColor(self,xLabel,yLabel):
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y]['color']

#-------------------------------------------------------------
	def putTitle(self,xLabel,yLabel,title):
		[x,y] = self.coord(xLabel, yLabel)
		self.gridList[x][y]['title'] = title
#-------------------------------------------------------------
	def getTitle(self,xLabel,yLabel):
		[x,y] = self.coord(xLabel, yLabel)
		return self.gridList[x][y]['title']


#-------------------------------------------------------------
	def HTML(self):

		html = ""
		for y in range(self.yLength) :
			html += "<tr>"
			for x in range(self.xLength) :
				data = self.gridList[x][y]['data']
				style = self.gridList[x][y]['style']
				color = self.gridList[x][y]['color']
				title = self.gridList[x][y]['title']
				if x==0 or y==0 :
					html += "<th title='{3}'  style='background-color:{0}; {1}'>{2}</th>".format(color,style,data,title)
				else :
					html += "<td title='{3}' style='background-color:{0};  {1}'>{2}</td>".format(color,style,data,title)

			html += "</tr>"
		return html

#-------------------------------------------------------------
























