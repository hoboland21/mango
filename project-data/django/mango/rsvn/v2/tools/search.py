from datetime import date,time 
from rsvn.models import *
from django.db.models import Q

#------------------
def search_query(post) :
#------------------
	result = {}	
	qlist = []  
	today = date.today().isoformat()
	for s in [ 'query','dquery'] :
		result[s] = ""
	if "query" in post and len(post['query']):
		q = post['query']
		qlist = Rsvn.objects.filter(Q(lastname__icontains=q)|Q(firstname__icontains=q)
			).order_by('-dateIn')

		if not "include_cancel" in post :
			qlist = qlist.exclude(status="cancel") 
		result["query"] = q	
	elif "dquery" in post and len(post['dquery']):
		dq = post["dquery"]
		dqlist = Rsvn.objects.filter(dateIn__lte = dq,dateOut__gte=dq).order_by('-dateIn')
		if not "include_cancel" in post :
			dqlist = dqlist.exclude(status="cancel") 
		qlist = dqlist	
		result["dquery"] = dq
	elif "xquery" in post:
		xql=[]
		xqlist = Rsvn.objects.filter(dateIn__gte = today).order_by('-dateIn')
		if not "include_cancel" in post :
			xqlist = xqlist.exclude(status="cancel") 
		
		for x in xqlist :
			if  not Room.objects.filter(rsvn__id=x.id) :
				xql.append(x)
		qlist = xql	
	else:
		qlist =''
	result['qlist']=qlist
	return result