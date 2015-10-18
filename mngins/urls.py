from django.conf.urls import patterns, include, url

from mngins.views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^modify_auths', modify_auths, name='modify_auths'),
    url(r'^modify_pinfo', modify_pinfo, name='modify_pinfo'),
    url(r'^itemtemp$', itemtemp, name='itemtemp'),
    url(r'^itemtemp_update$', itemtemp_update, name='itemtemp_update'),
    url(r'^itemtemp_category$', itemtemp_category, name='itemtemp_category'),
    url(r'^assesstemp$', assesstemp, name='assesstemp'),
    
)
