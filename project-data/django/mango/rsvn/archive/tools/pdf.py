#! /usr/bin/python

from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.units import mm,inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import cups

logo = "/usr/local/django/mango/static/rsvn/img/mangoSmall.jpg"
testpdf = "/usr/local/django/mango/static/rsvn/img/test.pdf"
width,height = letter
center_x = width/2


def printit():
    conn = cups.Connection()
    printer_name = conn.getPrinters().keys()[0]
    conn.printFile(printer_name,testpdf,"Python",{})

def new():
    c = canvas.Canvas(testpdf,pagesize=letter)
    c.drawImage(logo, 25, height-119,190,109)
    c.setStrokeGray(0.65)
    c.setFillGray(0.65)
    c.line(10,height-100,width-10,height-100)
    c.line(10,height-140,width-10,height-140)
    c.setFont("Helvetica-Bold",18)
    c.drawCentredString(center_x,height-125,"Reservation Form")
    return c
'''
    t = c.beginText()
    t.setFillColor('BurlyWood')
    t.setFont("Helvetica-Bold",22)
    t.setTextOrigin(200,600)
    t.textLine("Reservation Form")
    print t.getCursor()
    t.setFont("Helvetica-Bold",10)
    t.setFillColor('Black')
    t.moveCursor(-50,20)
    t.textLine("Customer Name")
    print t.getCursor()
    c.drawText(t)
   
	for offset in range(22) :
		x = offset*grid_spacing_x + left_margin
		y1 = height-150
		y2 = height-160
		c.line(x,y1,x,y2)
		c.drawRightString(x,y1,str(offset))

	for offset in range(31) :
		x1 = left_margin
		x2 = left_margin - 10
		y = top_margin - offset*grid_spacing_y  
		c.line(x1,y,x2,y)
		c.drawRightString(x2-3,y,str(offset))
'''	
def makepdf(c) :
    c.showPage()
    c.save()

	
def form_lines(c) :
	grid_spacing_x = 25
	grid_spacing_y = 40
	
	left_margin = 40
	top_margin = height - 175

	form_set = [
		["Date Received",0,3],
		["Source",1,3],
		["Tour Agent",2,3],

		["Check In",0,10],
		["Check Out",1,10],

		["Type",0,17],
		["Rooms",1,17],
		["Beds",2,17],


		["First Name",4,4],
		["Last Name",5,4],
		["Phone 1",6,4],
		["Phone 2",7,4],
		["City",8,4],
		["Country",9,4],

		["Adults",4,15],
		["Child",5,15],
		["Infant",6,15],

		["Notes",11,4],
		
		["Email",9,12],
	]
	for f in form_set :
		x = f[2]*grid_spacing_x + left_margin
		y = top_margin - f[1]*grid_spacing_y  
		c.drawRightString(x,y,f[0])
		
		
   
def heading() :
	c = new() 
	c.setFillGray(0.40)
	c.setFont("Helvetica-Bold",10)
	heading_text = (
		"Mango Resort Saipan",
		"P.O. Box 505478",
		"Saipan, MP 96950",
		"(670) 288-6903, 288-6904",
		"www.mangoresort.com" )	
	
	curr_line = height - 30
	right_margin = width - 20

	for line in heading_text :
		c.drawRightString(right_margin,curr_line,line)
		curr_line -= 13
	
	form_lines(c)
	makepdf(c)	
		
		
		
		
