from django.conf.urls import patterns, include, url

from tch.views import *

urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^$', main, name='main'),
    url(r'^modify_auth/$', modify_auth, name='modify_auth'),
    url(r'^modify_pinfo$', modify_pinfo, name='modify_pinfo'),
    url(r'^exam_result/', exam_result, name='exam_result'),
    url(r'^assess_mng/$', assess_mng, name='assess_mng'),
    url(r'^create_assesstemp_wiz1/$', create_assesstemp_wiz1, name='create_assesstemp_wiz1'),
    
)