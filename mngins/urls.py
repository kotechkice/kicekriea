from django.conf.urls import patterns, include, url

from mngins.views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^modify_auths', modify_auths, name='modify_auths'),
    
)
