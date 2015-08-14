from django.conf.urls import patterns, include, url

from mngins.views import *

urlpatterns = patterns('',
    url(r'^login$', login, name='login'),
)