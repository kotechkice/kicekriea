from django.conf.urls import patterns, include, url

from stdnt.views import *

urlpatterns = patterns('',
    url(r'^login$', login, name='login'),
    
)