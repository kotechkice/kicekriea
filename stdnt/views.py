from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_origin
from django.contrib.auth import logout as logout_origin
from django.utils import timezone

from stdnt import strings as stdnt_string
from home import strings as home_string

from assess.models import *
from assess.funcs import *

from stdnt.models import *
from stdnt.funcs import *

from auth_ext.models import *
from auth_ext.funcs import * 


import json

# Create your views here.
def login(request):
    if request.method == 'POST':
        data = json.dumps({'status':"fail", 'msg':'unknown error'})
        if 'email' in request.POST:
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                if 'pw' in request.POST:
                    pw =  request.POST['pw']
                    user = authenticate(username=user.username, password=pw)
                    if user is not None:
                        if user.is_active:
                            login_origin(request, user)
                            data = json.dumps({'status':"success", 'msg':'/stdnt'})
                        else:
                            # Return a 'disabled account' error message
                            data = json.dumps({'status':"fail", 'msg':'disabled account'})
                    else:
                        # Return an 'invalid login' error message.
                        data = json.dumps({'status':"fail", 'msg':'invalid login'})
                else:
                    data = json.dumps({'status':"fail", 'msg':'Enter the password.'})
            except ObjectDoesNotExist:
                data = json.dumps({'status':"fail", 'msg':'unknown email'})
        else:
            data = json.dumps({'status':"fail", 'msg':'Enter your email'})
            
        return HttpResponse(data, 'application/json')
    if request.user.is_authenticated():
        return redirect('/stdnt')
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
    })
    return render_to_response('stdnt/login.html', variables)

def main(request):
    if not request.user.is_authenticated():
        return redirect('/stdnt/login')
    
    my_info = request.user
    my_usergroupinfo_schools = my_info.usergroupinfo_set.filter(group__groupdetail__type='S')
    if len(my_usergroupinfo_schools) > 0:
        my_usergroupinfo_school = my_usergroupinfo_schools[0]
    else:
        my_usergroupinfo_school = None
    
    my_usergroupinfo_classes = my_info.usergroupinfo_set.filter(group__groupdetail__type='C')
    if len(my_usergroupinfo_classes) > 0:
        my_usergroupinfo_class = my_usergroupinfo_classes[0]
    else:
        my_usergroupinfo_class = None
    examlist = []
    
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo_class.group):
        examlist.append(ga.at)
        ua_list = UserAssessment.objects.filter(at=ga.at, user = my_info)
        examlist[-1].is_started = False
        examlist[-1].is_finished = False
        if len(ua_list) != 0:
            ua = ua_list[0]
            examlist[-1].is_started = True
            if ua.end_time != None:
                examlist[-1].is_finished = True
    '''
    examlist = ExamList.objects.all()
    for i in range(len(examlist)):
        ua_list = UserAssessment.objects.filter(at=examlist[i].at, user = my_info)
        examlist[i].is_started = False
        examlist[i].is_finished = False
        if len(ua_list) != 0:
            ua = ua_list[0]
            examlist[i].is_started = True
            if ua.end_time != None:
                examlist[i].is_finished = True
                ae_list = AssessEaxm.objects.filter(ua=ua)
                if len(ae_list) != 0:
                    ae = ae_list[0]
                    examlist[i].is_high = False
                    examlist[i].is_middle = False
                    examlist[i].is_low = False
                    examlist[i].is_fail = False
                    if ae.level == 'H':
                        examlist[i].help_str = examlist[i].help_h
                        examlist[i].is_high = True
                    elif ae.level == 'M':
                        examlist[i].help_str = examlist[i].help_m
                        examlist[i].is_middle = True
                    elif ae.level == 'L':
                        examlist[i].help_str = examlist[i].help_l
                        examlist[i].is_low = True
                    elif ae.level == 'F':
                        examlist[i].help_str = examlist[i].help_f
                        examlist[i].is_fail = True
                    examlist[i].level = stdnt_string.LEVEL[ae.level]
    '''
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        'examlist':examlist,
    })
    return render_to_response('stdnt/main.html', variables)

def logout(request):
    logout_origin(request)
    return redirect('/stdnt/login')

def register(request):
    if request.method == 'POST':
        data = json.dumps({'status':"fail", 'msg':'init data'})
        if 'email' in request.POST and 'firstname' in request.POST and 'lastname' in request.POST and 'clas_id' in request.POST and 'std_num' in request.POST:
            try:
                email=request.POST['email']
                clas_group = Group.objects.get(pk=request.POST['clas_id'])
                school_group = clas_group.groupdetail.upper_group.groupdetail.upper_group
                if adduser_createpw_sendmail(email=email, group=school_group, firstname=request.POST['firstname'], lastname=request.POST['lastname'], group_id=request.POST['std_num']):
                    new_std_group_info = UserGroupInfo()
                    new_std_group_info.user = User.objects.get(email=email)
                    new_std_group_info.group = clas_group
                    new_std_group_info.save()
                    data = json.dumps({'status':"success"})
                else:
                    data = json.dumps({'status':"fail", 'msg':'create error'})
            except:
                data = json.dumps({'status':"fail", 'msg':'no class'})
        else:
            data = json.dumps({'status':"fail", 'msg':'no data'})
        #data = json.dumps({'status':"success"})
        return HttpResponse(data, 'application/json')
    
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            return HttpResponse(data, 'application/json')
        
        if request.GET['method'] == 'sel_school':
            if 'id' in request.GET:
                school_id = request.GET['id']
                #school = Group.objects.get(pk=school_id)
                grades = Group.objects.filter(groupdetail__upper_group__pk = school_id, groupdetail__type = 'G')
                grades_data = [];
                for grade in grades:
                    grades_data.append((grade.id, grade.groupdetail.nickname))
                data = json.dumps({'status':"success", 'grades':grades_data})
            else:
                data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'sel_grade':
            if 'id' in request.GET:
                grade_id = request.GET['id']
                classes = Group.objects.filter(groupdetail__upper_group__pk = grade_id, groupdetail__type = 'C')
                classes_data = [];
                for clas in classes:
                    classes_data.append((clas.id, clas.groupdetail.nickname))
                data = json.dumps({'status':"success", 'classes':classes_data})
            else:
                data = json.dumps({'status':"fail"})
        return HttpResponse(data, 'application/json')
    
    
    schools = Group.objects.filter(groupdetail__type = 'S')
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'schools':schools,
    })
    return render_to_response('stdnt/register.html', variables) 

def modify_pinfo(request):
    if not request.user.is_authenticated():
        return redirect('/stdnt/login')
    my_info = request.user
    my_school_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    my_class_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='C')
    
    if request.method == 'POST':
        data = json.dumps({'status':"fail"})
        if 'origin_pw' in request.POST and 'new_pw' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST and 'school_id' in request.POST and 'clas_id' in request.POST and 'std_num' in request.POST:
            if my_info.check_password(request.POST['origin_pw']):
                if request.POST['new_pw'] != '':
                    my_info.set_password(request.POST['new_pw'])
                my_info.first_name = request.POST['first_name']
                my_info.last_name = request.POST['last_name']
                my_info.userdetail.full_name = my_info.last_name + my_info.first_name
                my_info.userdetail.save()
                my_info.save()
                my_school_usergroupinfo.user_id_of_group = request.POST['std_num']
                my_school_usergroupinfo.save()
                
                changed_school_group = Group.objects.get(pk=request.POST['school_id'])
                if my_school_usergroupinfo.group != changed_school_group:
                    my_school_usergroupinfo.group = changed_school_group
                    my_school_usergroupinfo.save()
                changed_clas_group = Group.objects.get(pk=request.POST['clas_id'])
                if my_class_usergroupinfo.group != changed_clas_group:
                    my_class_usergroupinfo.group = changed_clas_group
                    my_class_usergroupinfo.save()
                    
                data = json.dumps({'status':"success"})
            else:
                data = json.dumps({'status':"fail", 'msg':'password incorrect'})
        return HttpResponse(data, 'application/json')
    
    school_id = my_school_usergroupinfo.group.id
    grade_id = my_class_usergroupinfo.group.groupdetail.upper_group.id
    clas_id = my_class_usergroupinfo.group.id
    
    schools = Group.objects.filter(groupdetail__type='S')
    grades = Group.objects.filter(groupdetail__type='G', groupdetail__upper_group__id = school_id)
    classes = Group.objects.filter(groupdetail__type='C', groupdetail__upper_group__id = grade_id)
    std_num = my_school_usergroupinfo.user_id_of_group
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'std_num':std_num,
        'schools':schools,
        'school_id':school_id,
        'grades':grades,
        'grade_id':grade_id,
        'classes':classes,
        'clas_id':clas_id,
    })
    return render_to_response('stdnt/modify_pinfo.html', variables) 

def exam_list(request):
    if not request.user.is_authenticated():
        return redirect('/stdnt/login')

    my_info = request.user
    
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            return HttpResponse(data, 'application/json')
        if request.GET['method'] == 'call_ua':
            if 'at_id' in request.GET:
                at_id = request.GET['at_id']
                ua_list = UserAssessment.objects.filter(at__id = at_id, user = my_info, end_time=None)
                if len(ua_list) == 0:
                    at_list = AssessmentTemplate.objects.filter(pk=at_id)
                    if len(at_list) == 0:
                        data = json.dumps({'status':"fail"})
                    else:
                        data = json.dumps({'status':"success", 'ua_id':'empty', 'ct_id':at_list[0].ct_id})
                else:
                    data = json.dumps({'status':"success", 'ua_id':ua_list[0].id})
            else :
                data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'create_ua':
            if 'items' in request.GET and 'at_id' in request.GET and 'ci_id' in request.GET:
                items =  json.loads(request.GET['items'])
                at_list = AssessmentTemplate.objects.filter(pk=request.GET['at_id'])
                ua_id = create_ua_from_itemdict_N_at(at_list[0], items, my_info, request.GET['ci_id'])
                data = json.dumps({'status':"success", 'ua_id':ua_id})
        elif request.GET['method'] == 'get_itmes':
            if 'exam_order' in request.GET:
                items = {}
                el_list = ExamList.objects.filter(exam_order = request.GET['exam_order'])
                if len(el_list) != 0:
                    el = el_list[0]
                    ua_list = UserAssessment.objects.filter(at = el.at, user=my_info)
                    guis=[]
                    
                    if len(ua_list) != 0:
                        ua = ua_list[0]
                        guis = ua.gradeduseritem_set.order_by('order').all()
                        items['length'] = len(guis)
                        for gui in guis:
                            items[gui.order] ={
                                'item_id' : gui.it.cafa_it_id,
                                'seed' : gui.seed,
                                'permutation' : gui.permutation,
                                'item_permutation' : gui.item_permutation,
                                'choices_in_a_row' : gui.it.choices_in_a_row,
                                'response' : gui.response,
                                'correctanswer' : gui.correctanswer,
                                'is_correct' : gui.response == gui.correctanswer,
                            }
                    data = json.dumps({'status':"success", 'items':items})
        return HttpResponse(data, 'application/json')
    
    examlist = ExamList.objects.all()
    for i in range(len(examlist)):
        ua_list = UserAssessment.objects.filter(at=examlist[i].at, user = my_info)
        examlist[i].is_started = False
        examlist[i].is_finished = False
        if len(ua_list) != 0:
            ua = ua_list[0]
            examlist[i].is_started = True
            if ua.end_time != None:
                examlist[i].is_finished = True
                ae_list = AssessEaxm.objects.filter(ua=ua)
                if len(ae_list) != 0:
                    ae = ae_list[0]
                    examlist[i].is_high = False
                    examlist[i].is_middle = False
                    examlist[i].is_low = False
                    examlist[i].is_fail = False
                    if ae.level == 'H':
                        examlist[i].help_str = examlist[i].help_h
                        examlist[i].is_high = True
                    elif ae.level == 'M':
                        examlist[i].help_str = examlist[i].help_m
                        examlist[i].is_middle = True
                    elif ae.level == 'L':
                        examlist[i].help_str = examlist[i].help_l
                        examlist[i].is_low = True
                    elif ae.level == 'F':
                        examlist[i].help_str = examlist[i].help_f
                        examlist[i].is_fail = True
                    examlist[i].level = stdnt_string.LEVEL[ae.level]
                
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'examlist' : examlist,
        'examlist_len' : len(examlist),
        'my_info' : my_info,
    })
    return render_to_response('stdnt/exam_list.html', variables) 

def solve_itemeach(request, ua_id):
    if not request.user.is_authenticated():
        return redirect('/stdnt/login')
    
    ua = UserAssessment.objects.get(pk=ua_id);
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            return HttpResponse(data, 'application/json')
        if request.GET['method'] == 'init_order':
            order_num = 1
            if ua.solving_order_num != None:
                order_num = ua.solving_order_num
                num_item = ua.at.num_item
            responses_str = ''.join(map(lambda x:x.response, ua.gradeduseritem_set.all()))
            data = json.dumps({'status':"success", 'order':order_num, 'num_item':num_item, 'responses':responses_str})
        elif request.GET['method'] == 'get_itemid':
            if 'order' in request.GET:
                order_num=request.GET['order']
                gui = ua.gradeduseritem_set.get(order=order_num)
                itemid = gui.it.cafa_it_id
                ua.solving_order_num = order_num
                ua.save()
                data = json.dumps({
                    'status':"success", 
                    'itemid':itemid, 
                    'seed':gui.seed, 
                    'permutation':gui.permutation,
                    'response':gui.response,
                })
        elif request.GET['method'] == 'save_response':
            if 'order' in request.GET and 'response' in request.GET and 'add_seconds' in request.GET:
                order_num=request.GET['order']
                add_seconds = int(request.GET['add_seconds'])
                ua.solving_seconds += add_seconds
                ua.save()
                gui = ua.gradeduseritem_set.get(order=order_num)
                gui.response = request.GET['response']
                gui.elapsed_time += add_seconds
                gui.save()
                data = json.dumps({'status':"success"});
        elif request.GET['method'] == 'get_responses':
            responses_str = ''.join(map(lambda x:x.response, ua.gradeduseritem_set.all()))
            data = json.dumps({'status':"success", 'responses':responses_str, 'ci_id':ua.ci_id})
        elif request.GET['method'] == 'input_correctanswers':
            if 'correctanswers' in request.GET and ua.end_time == None:
                correctanswer_str = request.GET['correctanswers']
                ua.end_time = timezone.now()
                ua.save()
                for index in range(1, len(correctanswer_str)+1):
                    gui = ua.gradeduseritem_set.get(order=index)
                    gui.correctanswer = correctanswer_str[index-1]
                    gui.save()
                assess_user_by_exam(ua)
                data = json.dumps({'status':"success"});
        elif request.GET['method'] == 'set_permutation':
            if 'order' in request.GET and 'permutation_str' in request.GET:
                gui = ua.gradeduseritem_set.get(order=request.GET['order'])
                set_item_permutation_in_gui(gui, request.GET['permutation_str'])
                data = json.dumps({'status':"success", 'item_permutation':gui.item_permutation});
        return HttpResponse(data, 'application/json')
    
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'ua':ua
    })
    return render_to_response('stdnt/solve_itemeach.html', variables)

def report(request, at_id):
    if not request.user.is_authenticated():
        return redirect('/stdnt/login')
    
    myinfo = request.user
    at = AssessmentTemplate.objects.get(pk=at_id)
    ua_list = UserAssessment.objects.filter(at = at, user=myinfo)
    guis=[]
    if len(ua_list) != 0:
        ua = ua_list[0]
        guis = ua.gradeduseritem_set.order_by('order').all()
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'guis':guis,
    })
    return render_to_response('stdnt/report.html', variables)

