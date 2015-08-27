from django.conf.urls import patterns, include, url

from tch.views import *

urlpatterns = patterns('',
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^$', main, name='main'),
    url(r'^modify_auth$', modify_auth, name='modify_auth'),
)