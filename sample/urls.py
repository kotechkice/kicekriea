from django.conf.urls import patterns, include, url

from sample.views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^stdnt_assess_list$', stdnt_assess_list, name='stdnt_assess_list'),
    url(r'^stdnt_workbookprint$', stdnt_workbookprint, name='stdnt_workbookprint'),
    url(r'^stdnt_solve_responseonly', stdnt_solve_responseonly, name='stdnt_solve_responseonly'),
    url(r'^stdnt_solve_itemall$', stdnt_solve_itemall, name='stdnt_solve_itemall'),
    
    url(r'^tch_assess_mng$', tch_assess_mng, name='tch_assess_mng'),
    url(r'^tch_create_assesstemp_wiz1_1$', tch_create_assesstemp_wiz1_1, name='tch_create_assesstemp_wiz1_1'),
    url(r'^tch_create_assesstemp_wiz1_2$', tch_create_assesstemp_wiz1_2, name='tch_create_assesstemp_wiz1_2'),
    url(r'^tch_create_assesstemp_wiz1_3$', tch_create_assesstemp_wiz1_3, name='tch_create_assesstemp_wiz1_3'),
    url(r'^tch_create_assesstemp_wiz1_4$', tch_create_assesstemp_wiz1_4, name='tch_create_assesstemp_wiz1_4'),
    url(r'^tch_assess_status_assess', tch_assess_status_assess, name='tch_assess_status_assess'),
    url(r'^tch_assess_status_stdnt', tch_assess_status_stdnt, name='tch_assess_status_stdnt'),
    url(r'^tch_assess_status_time', tch_assess_status_time, name='tch_assess_status_time'),
    
    url(r'^mngins_assesstemp', mngins_assesstemp, name='mngins_assesstemp'),
    url(r'^mngins_create_assesstemp_wiz1', mngins_create_assesstemp_wiz1, name='mngins_create_assesstemp_wiz1'),
    url(r'^mngins_create_assesstemp_wiz2', mngins_create_assesstemp_wiz2, name='mngins_create_assesstemp_wiz2'),
    url(r'^mngins_create_assesstemp_wiz3', mngins_create_assesstemp_wiz3, name='mngins_create_assesstemp_wiz3'),
    url(r'^mngins_assess_status_assess', mngins_assess_status_assess, name='mngins_assess_status_assess'),
    url(r'^mngins_assess_status_ct', mngins_assess_status_ct, name='mngins_assess_status_ct'),
    url(r'^mngins_itemtemp_cartegory', mngins_itemtemp_cartegory, name='mngins_itemtemp_cartegory'),
    url(r'^mngins_itemtemp_edit', mngins_itemtemp_edit, name='mngins_itemtemp_edit'),
    
    
)