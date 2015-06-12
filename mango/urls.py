from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   url(r'^rsvn/', include('rsvn.urls')),	
   url(r'^accounts/login/', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout/', 'django.contrib.auth.views.logout'),
			
	
	url(r'^accounts/password_change/$','django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/rsvn/available'}, name="password_change"), 

	
    url(r'^admin/', include(admin.site.urls)),
)
