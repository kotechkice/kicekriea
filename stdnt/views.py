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
                    ua = ua_list[0]
                    start_time = ua.start_time
                    if ua.start_time == None:
                        start_time = 'empty'
                    else:
                        start_time = ua.start_time.strftime("%Y-%m-%d %H:%M")
                    data = json.dumps({
                        'status':"success", 
                        'ua_id':ua.id, 
                        'start_time':start_time, 
                        'ct_id':ua.at.ct_id
                    })
        elif request.GET['method'] == 'create_ua':
            if ('items' and 'at_id' and 'ci_id' and 'type') in request.GET:
                if request.GET['type'] == 'D' or request.GET['type'] == 'P':
                    items =  json.loads(request.GET['items'])
                    at_list = AssessmentTemplate.objects.filter(pk=request.GET['at_id'])
                    ua_id = create_ua_from_itemdict_N_at(at_list[0], items, my_info, request.GET['ci_id'])
                    ua = UserAssessment.objects.get(id=ua_id)
                    ua.type = 'D'
                    ua.save()
                    data = json.dumps({'status':"success", 'ua_id':ua_id})
        elif request.GET['method'] == 'create_gui':
            if ('items' and 'at_id' and 'ci_id' and 'ua_id') in request.GET:
                ua = UserAssessment.objects.get(id = request.GET['ua_id'])
                itemdict =  json.loads(request.GET['items'])
                at = AssessmentTemplate.objects.get(id=request.GET['at_id'])
                ua.ci_id = request.GET['ci_id']
                ua.start_time = timezone.now()
                ua.solving_order_num = 1
                ua.solving_seconds = 0
                ua.save()
                for index in range(1, len(itemdict)+1):
                    gui = GradedUserItem()
                    gui.ua = ua
                    itnum = int(itemdict[str(index)]['ItemID'])
                    exist_list = ItemTemplate.objects.filter(cafa_it_id=itnum)
                    if len(exist_list) == 0:
                        it = ItemTemplate()
                        it.cafa_it_id = itnum
                        it.save()
                    else:
                        it = exist_list[0]
                    gui.it = it
                    #it.choices_in_a_row = itemdict[str(index)]['NumChoices']
                    it.save()
                    gui.order = index
                    gui.seed = int(itemdict[str(index)]['Seed'])
                    gui.permutation = ''.join(itemdict[str(index)]['Permutation'].split(',')) 
                    gui.response = 'x'
                    gui.correctanswer = 'x'
                    gui.elapsed_time = 0
                    gui.save()
                data = json.dumps({'status':"success", 'ua_id':ua.id})
        return HttpResponse(data, 'application/json')
    
    def make_assess(data):
        ua_list = UserAssessment.objects.filter(at=data, user = my_info)
        data.is_started = False
        data.is_finished = False
        data.level = 'N'
        if len(ua_list) != 0:
            ua = ua_list[0]
            data.is_started = True
            if ua.end_time != None:
                data.is_finished = True
                data.level = ua.level
        return data
    examlist = []
    DS_examlist = []
    DU_examlist = []
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo_school.group, type = 'D'):
        examlist.append(make_assess(ga.at))
        if len(ga.at.get_itcs()) == 1:
            DS_examlist.append(make_assess(ga.at))
            DS_examlist[-1].itc = ga.at.get_itcs()[0]
        else:
            DU_examlist.append(make_assess(ga.at))
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo_class.group, type = 'D'):
        examlist.append(make_assess(ga.at))
        if len(ga.at.get_itcs()) == 1:
            DS_examlist.append(make_assess(ga.at))
            DS_examlist[-1].itc = ga.at.get_itcs()[0]
        else:
            DU_examlist.append(make_assess(ga.at))
    for ua in UserAssessment.objects.filter(user = my_info, type = 'D'):
        if not ua.at in examlist:
            examlist.append(make_assess(ua.at))
            if len(ua.at.get_itcs()) == 1:
                DS_examlist.append(make_assess(ua.at))
                DS_examlist[-1].itc = ua.at.get_itcs()[0]
            else:
                DU_examlist.append(make_assess(ua.at))
    D_examlist = examlist
    D_finished_len = len([x for x in examlist if x.is_finished == True])
    D_not_finished_len = len(examlist) - D_finished_len
    
    examlist = []
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo_school.group, type = 'P'):
        examlist.append(make_assess(ga.at))
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo_class.group, type = 'P'):
        examlist.append(make_assess(ga.at))
    for ua in UserAssessment.objects.filter(user = my_info, type = 'P'):
        if not ua.at in examlist:
            examlist.append(make_assess(ua.at))
    P_examlist = examlist
    P_finished_len = len([x for x in examlist if x.is_finished == True])
    P_not_finished_len = len(examlist) - P_finished_len
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        'D_examlist':D_examlist,
        'D_finished_len':D_finished_len,
        'D_not_finished_len':D_not_finished_len,
        'DS_examlist':DS_examlist,
        'DU_examlist':DU_examlist,
        'P_examlist':P_examlist,
        'P_finished_len':P_finished_len,
        'P_not_finished_len':P_not_finished_len,
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
            if ('items' and 'at_id' and 'ci_id' and 'type') in request.GET:
                if request.GET['type'] == 'D' or request.GET['type'] == 'P':
                    items =  json.loads(request.GET['items'])
                    at_list = AssessmentTemplate.objects.filter(pk=request.GET['at_id'])
                    #ua_id = create_ua_from_itemdict_N_at(at_list[0], items, my_info, request.GET['ci_id'])
                    #ua = UserAssessment.objects.get(id=ua_id)
                    #ua.type = 'D'
                    #ua.save()
                    #data = json.dumps({'status':"success", 'ua_id':ua_id})
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
            num_item = ua.at.num_item
            if ua.solving_order_num != None:
                order_num = ua.solving_order_num
                
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
                #assess_user_by_exam(ua)
                ua.assess_level()
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

def diagnosis_result(request):
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
    
    finished_ua_list = UserAssessment.objects.filter(user=my_info, type='D').exclude(end_time=None)
    s_ua_list = [] # standard
    u_ua_list = [] # unit
    for ua in finished_ua_list:
        ua_itcs = ua.at.get_itcs()
        if len(ua_itcs) == 1: # standard
            s_ua = ua
            s_ua.itc = ua_itcs[0]
            
            itclhs = ItemTemplateCategoryLevelHelp.objects.filter(itc=ua.itc)
            
            s_ua.levelhelp = 'None'
            if len(itclhs) != 0:
                if s_ua.level == 'H':
                    s_ua.levelhelp = itclhs[0].help_h
                elif s_ua.level == 'I':
                    s_ua.levelhelp = itclhs[0].help_m
                elif s_ua.level == 'E':
                    s_ua.levelhelp = itclhs[0].help_l
                elif s_ua.level == 'F':
                    s_ua.levelhelp = itclhs[0].help_f
            s_ua_list.append(ua)
        else:# unit
            ua.itcs = []
            ua.percent_point_all = int(round(ua.percent_point_all() * 100))
            for ua_itc in ua_itcs:
                ua.itcs.append({
                    'name':ua_itc.name,
                    'description':ua_itc.description,
                    'percent_point': int(round(ua.percent_point_itc(ua_itc) * 100))
                })
            ua.rowspan = len(ua_itcs) + 1
            u_ua_list.append(ua)
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        's_ua_list':s_ua_list,
        'u_ua_list':u_ua_list,
    })
    return render_to_response('stdnt/diagnosis_result.html', variables)

def practice_result(request):
    my_info = request.user
    my_usergroupinfo_schools = my_info.usergroupinfo_set.filter(group__groupdetail__type='S')
    
    
    finished_ua_list = UserAssessment.objects.filter(user=my_info, type='P').exclude(end_time=None)
    ua_list = []
    for ua in finished_ua_list:
        ua_itcs = ua.at.get_itcs()
        ua.itcs = []
        ua.percent_point_all = int(round(ua.percent_point_all() * 100))
        for ua_itc in ua_itcs:
            ua.itcs.append({
                'name':ua_itc.name,
                'description':ua_itc.description,
                'percent_point': int(round(ua.percent_point_itc(ua_itc) * 100))
            })
        ua.rowspan = len(ua_itcs) + 1
        ua_list.append(ua)
    
    if len(my_usergroupinfo_schools) > 0:
        my_usergroupinfo_school = my_usergroupinfo_schools[0]
    else:
        my_usergroupinfo_school = None
    
    my_usergroupinfo_classes = my_info.usergroupinfo_set.filter(group__groupdetail__type='C')
    if len(my_usergroupinfo_classes) > 0:
        my_usergroupinfo_class = my_usergroupinfo_classes[0]
    else:
        my_usergroupinfo_class = None
    
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        'ua_list':ua_list,
    })
    return render_to_response('stdnt/practice_result.html', variables)

def print_assess(request, ua_id):
    #if not request.user.is_authenticated():
    #    return redirect('/stdnt/login')
    
    #my_info = request.user
    ua = UserAssessment.objects.get(id=ua_id)
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
        
        if request.GET['method'] == 'get_item_info':
            if 'itemid' in request.GET:
                it = ItemTemplate.objects.get(cafa_it_id = request.GET['itemid'])
                data = json.dumps({'status':'success', 'choices_in_a_row':it.choices_in_a_row})
        return HttpResponse(data, 'application/json')
    
    #ua.gradeduseritem_set.order_by('order').all()
    #responses_str = ''.join(map(lambda x:x.response, ua.gradeduseritem_set.all()))
    #item_ids_str = ', '.join(map(lambda x:str(x.it.cafa_it_id), ua.gradeduseritem_set.all()))
    item_ids = map(lambda x:x.it.cafa_it_id, ua.gradeduseritem_set.order_by('order').all())
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'ua_id':ua_id,
        'ua':ua,
        'item_ids':json.dumps(item_ids),
        #'my_info':my_info,
    })
    return render_to_response('stdnt/print_assess.html', variables)

def input_response(request, ua_id):
    ua = UserAssessment.objects.get(id=ua_id)
    item_info = []
    
    #for gui in ua.gradeduseritem_set.order_by('order').all():
    #    pass
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        #'ua_id':ua_id,
        'ua':ua,
        'guis':ua.gradeduseritem_set.order_by('order').all(),
        
        #'item_ids':json.dumps(item_ids),
        #'my_info':my_info,
    })
    return render_to_response('stdnt/input_response.html', variables)

def diagnosis_ans(request):
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
    
    
    finished_ua_list = UserAssessment.objects.filter(user=my_info, type='D').exclude(end_time=None)
    s_ua_list = [] # standard
    u_ua_list = [] # unit
    for ua in finished_ua_list:
        ua_itcs = ua.at.get_itcs()
        if len(ua_itcs) == 1: # standard
            s_ua = ua
            s_ua.itc = ua_itcs[0]
            s_ua.guis = ua.gradeduseritem_set.order_by('order').all()
            for i in range(len(s_ua.guis)):
                s_ua.guis[i].correct = s_ua.guis[i].response == s_ua.guis[i].correctanswer
            s_ua_list.append(s_ua)
        else:# unit
            u_ua = ua
            u_ua.guis = ua.gradeduseritem_set.order_by('order').all()
            for i in range(len(u_ua.guis)):
                u_ua.guis[i].correct = u_ua.guis[i].response == u_ua.guis[i].correctanswer
            #ua.percent_point_all = int(round(ua.percent_point_all() * 100))
            #ua.rowspan = len(ua_itcs) + 1
            u_ua_list.append(u_ua)
            
            
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        's_ua_list':s_ua_list,
        'u_ua_list':u_ua_list,
    })
    return render_to_response('stdnt/diagnosis_ans.html', variables)

def practice_ans(request):
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
    
    finished_ua_list = UserAssessment.objects.filter(user=my_info, type='P').exclude(end_time=None)
    u_ua_list = [] # unit
    for ua in finished_ua_list:
        u_ua = ua
        u_ua.guis = ua.gradeduseritem_set.order_by('order').all()
        for i in range(len(u_ua.guis)):
            u_ua.guis[i].correct = u_ua.guis[i].response == u_ua.guis[i].correctanswer
        u_ua_list.append(u_ua)
      
            
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
        'my_info':my_info,
        'my_usergroupinfo_school':my_usergroupinfo_school,
        'u_ua_list':u_ua_list,
    })
    return render_to_response('stdnt/practice_ans.html', variables)

def show_solution(request):
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
    })
    return render_to_response('stdnt/show_solution.html', variables)

def test_another_aig_item(request):
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
    })
    return render_to_response('stdnt/test_another_aig_item.html', variables)
    