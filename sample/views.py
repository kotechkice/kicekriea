from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext

# Create your views here.
def main(request):
    return render_to_response('sample/main.html')

def stdnt_assess_list(request):
    return render_to_response('sample/stdnt_assess_list.html')

def stdnt_workbookprint(request):
    return render_to_response('sample/stdnt_workbookprint.html')

def stdnt_solve_responseonly(request):
    return render_to_response('sample/stdnt_solve_responseonly.html')

def stdnt_solve_itemall(request):
    return render_to_response('sample/stdnt_solve_itemall.html')

def stdnt_exam_list(request):
    return render_to_response('sample/stdnt_exam_list.html')



def tch_assess_mng(request):
    return render_to_response('sample/tch_assess_mng.html')

def tch_create_assesstemp_wiz1_1(request):
    return render_to_response('sample/tch_create_assesstemp_wiz1_1.html')

def tch_create_assesstemp_wiz1_2(request):
    return render_to_response('sample/tch_create_assesstemp_wiz1_2.html')

def tch_create_assesstemp_wiz1_3(request):
    return render_to_response('sample/tch_create_assesstemp_wiz1_3.html')

def tch_create_assesstemp_wiz1_4(request):
    return render_to_response('sample/tch_create_assesstemp_wiz1_4.html')

def tch_assess_status_assess(request):
    return render_to_response('sample/tch_assess_status_assess.html')

def tch_assess_status_stdnt(request):
    return render_to_response('sample/tch_assess_status_stdnt.html')

def tch_assess_status_time(request):
    return render_to_response('sample/tch_assess_status_time.html')

def tch_exam_result(request):
    return render_to_response('sample/tch_exam_result.html')



def mngins_assesstemp(request):
    return render_to_response('sample/mngins_assesstemp.html')

def mngins_create_assesstemp_wiz1(request):
    return render_to_response('sample/mngins_create_assesstemp_wiz1.html')

def mngins_create_assesstemp_wiz2(request):
    return render_to_response('sample/mngins_create_assesstemp_wiz2.html')

def mngins_create_assesstemp_wiz3(request):
    return render_to_response('sample/mngins_create_assesstemp_wiz3.html')

def mngins_assess_status_assess(request):
    return render_to_response('sample/mngins_assess_status_assess.html')

def mngins_assess_status_ct(request):
    return render_to_response('sample/mngins_assess_status_ct.html')

def mngins_itemtemp_cartegory(request):
    return render_to_response('sample/mngins_itemtemp_cartegory.html')

def mngins_itemtemp_edit(request):
    return render_to_response('sample/mngins_itemtemp_edit.html')

