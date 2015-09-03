from django.conf.urls import patterns, include, url

from stdnt.views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^register$', register, name='register'),
    url(r'^modify_pinfo$', modify_pinfo, name='modify_pinfo'),
)