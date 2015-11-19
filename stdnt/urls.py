from django.conf.urls import patterns, include, url

from stdnt.views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^modify_pinfo/$', modify_pinfo, name='modify_pinfo'),
    url(r'^exam_list/$', exam_list, name='exam_list'),
    url(r'^solve_itemeach/([0-9]+)/$', solve_itemeach, name='solve_itemeach'),
    url(r'^report/([0-9]+)/$', report, name='report'),
    url(r'^diagnosis_result/$', diagnosis_result, name='diagnosis_result'),
    url(r'^practice_result/$', practice_result, name='practice_result'),
    url(r'^print_assess/([0-9]+)/$', print_assess, name='print_assess'),
    url(r'^input_response/([0-9]+)/$', input_response, name='input_response'),
    url(r'^diagnosis_ans/$', diagnosis_ans, name='diagnosis_ans'),
    url(r'^show_solution/$', show_solution, name='show_solution'),
    url(r'^test_another_aig_item/$', test_another_aig_item, name='test_another_aig_item'),
    url(r'^practice_ans/$', practice_ans, name='practice_ans'),
    
)