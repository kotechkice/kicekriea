from django.conf.urls import patterns, include, url

from tch.views import *

urlpatterns = patterns('',
    url(r'^login$', login, name='login'),
)