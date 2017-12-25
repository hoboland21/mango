from django.conf.urls import  url
from  rsvn import views
from rsvn.vc import  event, calendar, agent, detailEdit, detailList, chat, service, grid, occupancy, available, current,invoice,rates,webres,excelView

urlpatterns = [
    url(r'^$', views.index, name='index'),

	url(r'^detail/list/(?P<rsvnid>\d+)/$',detailList.RsvnList.as_view(), name='rsvnlist'),
	url(r'^detail/create/$',detailEdit.RsvnCreate.as_view(), name='rsvncreate'),

	url(r'^detail/update/(?P<rsvnid>\d+)/$',detailEdit.RsvnUpdate.as_view(), name='rsvnupdate'),

	url(r'^events/$',event.EventView.as_view(), name='events'),
	url(r'^calendar/(?P<rsvnid>\d+)/$',calendar.CalView.as_view(), name='calendar'),
	url(r'^service/$',service.ServiceView.as_view(), name='service'),
	url(r'^grid/(?P<rsvnid>\d+)/$',grid.gridView.as_view(), name='grid'),
	url(r'^invoice/(?P<rsvnid>\d+)/$',invoice.invoiceView.as_view(), name='invoice'),

	url(r'^rates/$',rates.RatesView.as_view(), name='rates'),

	url(r'^agents/$',agent.AgentView.as_view(), name='agents'),
	url(r'^chat/$',chat.ChatView.as_view(), name='chat'),
	url(r'^log/$',chat.LogView.as_view(), name='log'),
	url(r'^occupancy/$',occupancy.occupancyView.as_view(), name='occupancy'),

	url(r'^available/$',available.availableView.as_view(), name='available'),

	url(r'^current/$',current.currentView.as_view(), name='current'),
	url(r'^webres/$',webres.WebResView.as_view(), name='webres'),
	url(r'^webres/(?P<webid>\d+)/$',webres.WebMake.as_view(), name='webmake'),

	url(r'^excel/$',excelView.ExcelView.as_view(), name='excel')

#	url(r'^gridView/(?P<rsvnid>\d+)/$', views.gridViewRsvn, name='gridViewRsvn'),
#	url(r'^seperate/(?P<rsvnid>\d+)/$',views.seperate, name='seperate'),
#	 url(r'^(?P<rsvnid>\d+)/$', views.detail, name='detail'),

]