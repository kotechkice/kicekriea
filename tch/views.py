from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_origin
from django.contrib.auth import logout as logout_origin

from home import strings as home_string
from tch import strings as tch_string
from home.funcs import code_str_generator

from auth_ext.models import *
from auth_ext.funcs import * 

from assess.models import *
from assess.funcs import *

from stdnt.models import *
from stdnt import strings as stdnt_string
    
from datetime import datetime, date
import json

import pytz
from project import settings

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
                            data = json.dumps({'status':"success", 'msg':'/tch'})
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
        return redirect('/tch')
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
    })
    return render_to_response('tch/login.html', variables)

def main(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    my_info.is_groupsuperuser = my_usergroupinfo.is_groupsuperuser
    
    super_tch = UserGroupInfo.objects.get(group = my_usergroupinfo.group, is_groupsuperuser=True).user
    
    tg = request.user.usergroupinfo_set.get(group__groupdetail__type='T').group
    tch_len = len(UserGroupInfo.objects.filter(group = tg))
    
    classes = Group.objects.filter(groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="C")
    class_len = len(classes)
    std_len = 0
    for index in range(class_len):
        std_len += len(classes[index].usergroupinfo_set.all())
    
    len_P = len(AssessmentTemplate.objects.filter(owner_group = my_usergroupinfo.group, type='P'))
    len_D = len(AssessmentTemplate.objects.filter(owner_group = my_usergroupinfo.group, type='D'))
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info' : my_info,
        'my_usergroupinfo' : my_usergroupinfo,
        'super_tch':super_tch,
        'tch_len':tch_len,
        'class_len':class_len,
        'std_len':std_len,
        'len_P':len_P,
        'len_D':len_D,
    })
    return render_to_response('tch/main.html', variables)

def logout(request):
    logout_origin(request)
    return redirect('/tch/login')


def modify_auth(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    if not my_usergroupinfo.is_groupsuperuser:
        return redirect('/mngins/logout')
     
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
        
        if request.GET['method'] == 'add_new_tch':
            if 'email' in request.GET and 'firstname' in request.GET and 'lastname' in request.GET and 'comnum' in request.GET:
                email = request.GET['email']
                firstname = request.GET['firstname']
                lastname = request.GET['lastname']
                comnum = request.GET['comnum']
                
                group = request.user.usergroupinfo_set.get(group__groupdetail__type='S').group
                #data = json.dumps({'status':"success"})
                if adduser_createpw_sendmail(email=email, group=group, firstname=firstname, lastname=lastname, group_id=comnum):
                    new_tch_group_info = UserGroupInfo()
                    new_tch_group_info.user = User.objects.get(email=email)
                    new_tch_group_info.group = request.user.usergroupinfo_set.get(group__groupdetail__type='T').group
                    new_tch_group_info.save()
                    data = json.dumps({'status':"success"})
                else:
                    data = json.dumps({'status':"fail"})
            else:
                data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'add_new_class':
            if 'grade' in request.GET and 'class' in request.GET:
                create_class_in_school(my_usergroupinfo.group, request.GET['grade'], request.GET['class'])
                data = json.dumps({'status':"success"})
        elif request.GET['method'] == 'change_class_info':
            if ('class_id' and 'grade' and 'class') in request.GET:
                clas = Group.objects.get(id=request.GET['class_id'])
                change_class_in_school(clas, my_usergroupinfo.group, request.GET['grade'], request.GET['class'])
                data = json.dumps({'status':"success"})
        elif request.GET['method'] == 'del_class':
            if 'class_id' in request.GET:
                clas = Group.objects.get(id=request.GET['class_id'])
                clas.delete()
                data = json.dumps({'status':"success"})
        elif request.GET['method'] == 'send_newpw':
            if 'email' in request.GET:
                email = request.GET['email']
                if createpassword_sendmail(email):
                    data = json.dumps({'status':"success"})
        elif request.GET['method'] == 'del_auth':
            if 'email' in request.GET:
                u = User.objects.get(email=request.GET['email'])
                UserGroupInfo.objects.filter(user=u).delete()
                data = json.dumps({'status':"success"})
        return HttpResponse(data, 'application/json')
    
    tg = request.user.usergroupinfo_set.get(group__groupdetail__type='T').group
    tchs = map(lambda x:x.user, UserGroupInfo.objects.filter(group=tg))
    for index in range(len(tchs)):
        tchs_usergroupinfo =  tchs[index].usergroupinfo_set.get(group__groupdetail__type='S')
        tchs[index].comnum = tchs_usergroupinfo.user_id_of_group
        tchs[index].is_groupsuperuser = tchs_usergroupinfo.is_groupsuperuser
    
    #grades = Group.objects.filter(groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="G")
    classes = Group.objects.filter(groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="C")
    for index in range(len(classes)):
        classes[index].members_length = len(classes[index].usergroupinfo_set.all())
        
    ugi = UserGroupInfo.objects.filter(group__groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, group__groupdetail__type="C")
    students = map(lambda x:x.user, ugi)
    
    for index in range(len(students)):
        students[index].classname = students[index].usergroupinfo_set.get(group__groupdetail__type="C").group.groupdetail.nickname
        students[index].gradename = students[index].usergroupinfo_set.get(group__groupdetail__type="C").group.groupdetail.upper_group.groupdetail
        students[index].stdnum = students[index].usergroupinfo_set.get(group__groupdetail__type="S").user_id_of_group
    input_code = code_str_generator(size=4)
    
    variables = RequestContext(request, {
        'tchs' : tchs,
        'tch_len': len(tchs),
        'classes' : classes,
        'class_len' : len(classes),
        'students' : students,
        'std_len' : len(students),
        'input_code' : input_code,
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_usergroupinfo':my_usergroupinfo,
        'my_info':my_info,
    })
    return render_to_response('tch/modify_auth.html', variables)

def modify_pinfo(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    if request.method == 'POST':
        data = json.dumps({'status':"fail"})
        if 'origin_pw' in request.POST and 'new_pw' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST and 'comnum' in request.POST:
            if my_info.check_password(request.POST['origin_pw']):
                if request.POST['new_pw'] != '':
                    my_info.set_password(request.POST['new_pw'])
                my_info.first_name = request.POST['first_name']
                my_info.last_name = request.POST['last_name']
                my_info.userdetail.full_name = my_info.last_name + my_info.first_name
                my_info.userdetail.save()
                my_info.save()
                my_usergroupinfo.user_id_of_group = request.POST['comnum']
                my_usergroupinfo.save()
                data = json.dumps({'status':"success"})
            else:
                data = json.dumps({'status':"fail"})
        return HttpResponse(data, 'application/json')
    
    comnum = my_usergroupinfo.user_id_of_group
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info' : my_info,
        'comnum' : comnum,
    })
    return render_to_response('tch/modify_pinfo.html', variables)

def exam_result(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    ugi = UserGroupInfo.objects.filter(group__groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, group__groupdetail__type="C")
    students = map(lambda x:x.user, ugi)
    
    
    els = ExamList.objects.all()
    for index in range(len(els)):
        els[index].students_num = len(AssessEaxm.objects.filter(user__in = students, ua__at = els[index].at))
    ats = map(lambda x:x.at, els)
    aes = AssessEaxm.objects.filter(user__in = students, ua__at__in = ats)
    for index in range(len(aes)):
        aes[index].std_classname = aes[index].user.usergroupinfo_set.get(group__groupdetail__type="C").group.groupdetail.nickname
        aes[index].std_gradename = aes[index].user.usergroupinfo_set.get(group__groupdetail__type="C").group.groupdetail.upper_group.groupdetail
        aes[index].std_num = aes[index].user.usergroupinfo_set.get(group__groupdetail__type="S").user_id_of_group
        aes[index].standard = ExamList.objects.filter(at=aes[index].ua.at)[0].standard
        aes[index].level_str = stdnt_string.LEVEL[aes[index].level]
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'els' : els,
        'aes' : aes,
        'students_num' : len(students),
    })
    return render_to_response('tch/exam_result.html', variables)

def assess_mng(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info' : my_info,
        'my_usergroupinfo' : my_usergroupinfo,
    })
    return render_to_response('tch/assess_mng.html', variables)

def create_assesstemp_wiz1(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
        
        if request.GET['method'] == 'get_items':
            if 'selected_id' in request.GET:
                def get_its_from_itc(itc_id):
                    mitcs = MappedItemTemplateCategory.objects.filter(itc__id = itc_id)
                    its = map(lambda x:x.it, mitcs)
                    itcs = ItemTemplateCategory.objects.filter(upper_itc__id=itc_id)
                    ret_val = its
                    for itc in itcs:
                        ret_val += get_its_from_itc(itc.id)
                    return ret_val
                its = get_its_from_itc(request.GET['selected_id'])
                it_infos = []
                for it in its:
                    it_infos.append({
                        'itemid':it.cafa_it_id, 
                        'difficulty':it.difficulty, 
                        'ability':it.ability
                    })
                data = json.dumps({'status':'success', 'it_infos':it_infos})
        if request.GET['method'] == 'save_assess':
            if ('assess_name' and 'item_ids' and 'type') in request.GET:
                item_ids = json.loads(request.GET['item_ids'])
                
                at = AssessmentTemplate()
                at.name = request.GET['assess_name']
                at.creator = my_info
                at.owner_group = my_usergroupinfo.group
                at.num_item = len(item_ids)
                at.num_item_template = len(item_ids)
                at.type = request.GET['type']
                
                at.save()
                
                create_its_from_itnum_list_N_at(at, item_ids)
                data = json.dumps({'status':'success'})
        if request.GET['method'] == 'sel_itc':
            if ('itc_id') in request.GET:
                itc = ItemTemplateCategory.objects.get(id=request.GET['itc_id'])
                belong_itc_objects = ItemTemplateCategory.objects.filter(upper_itc=itc)
                belong_itcs = []
                for belong_itc_object in belong_itc_objects:
                    belong_itcs.append({ 'id':belong_itc_object.id, 'name':belong_itc_object.name})
                data = json.dumps({'status':'success', 'belong_itcs':belong_itcs})
        return HttpResponse(data, 'application/json')
    
    itcll0_s = ItemTemplateCategoryLevelLabel.objects.get(level=0)
    itc0_open = ItemTemplateCategory.objects.filter(level_label = itcll0_s, order=1)
    itc1_s = ItemTemplateCategory.objects.filter(upper_itc=itc0_open).order_by('order')
    itc2_s = ItemTemplateCategory.objects.filter(upper_itc = itc1_s[0]).order_by('order')
    itc3_s = ItemTemplateCategory.objects.filter(upper_itc = itc2_s[0]).order_by('order')
    itc4_s = ItemTemplateCategory.objects.filter(upper_itc = itc3_s[0]).order_by('order')
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info' : my_info,
        'my_usergroupinfo' : my_usergroupinfo,
        #'itc0_s':itc0_s,
        'itc1_s':itc1_s,
        'itc2_s':itc2_s,
        'itc3_s':itc3_s,
        'itc4_s':itc4_s,
    })
    return render_to_response('tch/create_assesstemp_wiz1.html', variables)

def assess_preview(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
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
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
    })
    return render_to_response('tch/assess_preview.html', variables)



def create_assesstemp_wiz2(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
       
        if request.GET['method'] == 'get_std_info':
            if 'clas_id' in request.GET:
                clas_stds = []
                for ugi in UserGroupInfo.objects.filter(group__id=request.GET['clas_id']):
                    clas_stds.append({'id':ugi.user.id, 'name':ugi.user.userdetail.full_name})
                
                data = json.dumps({'status':'success', 'clas_stds':clas_stds})
        if request.GET['method'] == 'get_ctid_and_set_assessment':
            if ('at_id' and 'group_unit' and 'assess_type' and 'ids' and 'start' and 'end') in request.GET:
                at = AssessmentTemplate.objects.get(id=request.GET['at_id'])
                if not at.ct_id:
                    miats = MappedItemAssessmentTemplate.objects.filter(at=at)
                    item_ids = []
                    for miat in miats:
                        item_ids.append(miat.it.cafa_it_id)
                        
                    random = str(int(at.is_random_order))+str(int(at.is_fixed_item))+str(int(at.is_random_choice_order))
                    data = json.dumps({
                        'status':'success',
                        'ct_id':'empty', 
                        'name':at.name, 
                        'item_ids':item_ids,
                        'random':random,
                    })
                else:
                    local_tz = pytz.timezone(settings.TIME_ZONE)
                    if request.GET['group_unit'] == 'A':
                        ga = GroupAssessment()
                        ga.group = my_usergroupinfo.group
                        ga.at = at
                        ga.type = request.GET['assess_type']
                        ga.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                        ga.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                        ga.save()
                    elif request.GET['group_unit'] == 'C':
                        ids = json.loads(request.GET['ids'])
                        for id in ids:
                            ga = GroupAssessment()
                            ga.group = Group.objects.get(id=id)
                            ga.at = at
                            ga.type = request.GET['assess_type']
                            ga.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                            ga.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                            ga.save()
                    elif request.GET['group_unit'] == 'S':
                        ids = json.loads(request.GET['ids'])
                        for user_id in ids:
                            ua = UserAssessment()
                            ua.user = User.objects.get(id=user_id)
                            ua.at = at
                            ua.type = request.GET['assess_type']
                            ua.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                            ua.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                            ua.save()
                            
                    data = json.dumps({'status':'success', 'ct_id':at.ct_id})
        if request.GET['method'] == 'set_ct_id_and_at':
            if ('at_id' and 'ct_id' and 'group_unit' and 'assess_type' and 'ids' and 'start' and 'end') in request.GET:
                at = AssessmentTemplate.objects.get(id=request.GET['at_id'])
                at.ct_id = request.GET['ct_id']
                #print request.GET['ct_id']
                at.save()
                local_tz = pytz.timezone(settings.TIME_ZONE)
                if request.GET['group_unit'] == 'A':
                    ga = GroupAssessment()
                    ga.group = my_usergroupinfo.group
                    ga.at = at
                    ga.type = request.GET['assess_type']
                    ga.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                    ga.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                    ga.save()
                elif request.GET['group_unit'] == 'C':
                    ids = json.loads(request.GET['ids'])
                    for id in ids:
                        ga = GroupAssessment()
                        ga.group = Group.objects.get(id=id)
                        ga.at = at
                        ga.type = request.GET['assess_type']
                        ga.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                        ga.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                        ga.save()
                elif request.GET['group_unit'] == 'S':
                    ids = json.loads(request.GET['ids'])
                    for user_id in ids:
                        ua = UserAssessment()
                        ua.user = User.objects.get(id=user_id)
                        ua.at = at
                        ua.type = request.GET['assess_type']
                        ua.period_start = local_tz.localize(datetime.strptime(request.GET['start'], "%Y-%m-%d %H:%M"))
                        ua.period_end = local_tz.localize(datetime.strptime(request.GET['end'], "%Y-%m-%d %H:%M"))
                        ua.save()
                        
                data = json.dumps({'status':'success'})
        return HttpResponse(data, 'application/json')
    
    ats = AssessmentTemplate.objects.filter(owner_group=my_usergroupinfo.group)
    
    classes = Group.objects.filter(groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="C")
    for index in range(len(classes)):
        classes[index].members_length = len(classes[index].usergroupinfo_set.all())
    
    first_clas = classes[0]
    first_clas_stds = []
    for ugi in UserGroupInfo.objects.filter(group=first_clas):
        first_clas_stds.append({'id':ugi.user.id, 'name':ugi.user.userdetail.full_name})
    
    date_now = datetime.now()
    start = {'date' : date_now.strftime("%Y-%m-%d"), 'time' : date_now.strftime("%I:%M %p")}
    next_month = datetime(date_now.year,date_now.month+1, date_now.day)
    end = {'date' : next_month.strftime("%Y-%m-%d"), 'time' : start['time'] }
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info':my_info,
        'my_usergroupinfo':my_usergroupinfo,
        'ats':ats,
        'classes':classes,
        'first_clas_stds':json.dumps(first_clas_stds),
        'first_clas_stds_length':len(first_clas_stds),
        'start':start,
        'end':end,
    })
    return render_to_response('tch/create_assesstemp_wiz2.html', variables)


def kice_assess_result(request):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    classes = Group.objects.filter(groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="C")
    
    def get_finished_std_num(at, school):
        std_list = []
        finished_std_num = 0
        gas = GroupAssessment.objects.filter(at = at)
        for ga in gas:
            ugis = UserGroupInfo.objects.filter(group = ga.group)
            for ugi in ugis:
                if not ugi.user in std_list:
                    std_list.append(ugi.user)
        ugis = UserGroupInfo.objects.filter(group = school)
        for ugi in ugis:
            uas = UserAssessment.objects.filter(at=at, user=ugi.user)
            if len(uas) != 0 and not ugi.user in std_list:
                std_list.append(ugi.user)
        for std in std_list:
            uas = UserAssessment.objects.filter(at=at, user=std)
            if len(uas) != 0 and uas[0].end_time != None:
                finished_std_num+=1
        #print std_list
        std_num = len(std_list)
        finish_rate = finished_std_num*100/std_num
        return finished_std_num, std_num, finish_rate
    
    examlist = []
    DS_examlist = []
    DU_examlist = []
    
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo.group, type = 'D'):
        examlist.append(ga.at)
        exam = ga.at
        exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ga.at, my_usergroupinfo.group)
        if len(ga.at.get_itcs()) == 1:
            DS_examlist.append(exam)
        else:
            DU_examlist.append(exam)
    for clas in classes:
        for ga in GroupAssessment.objects.filter(group = clas, type = 'D'):
            examlist.append(ga.at)
            exam = ga.at
            exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ga.at, my_usergroupinfo.group)
            if len(ga.at.get_itcs()) == 1:
                DS_examlist.append(exam)
            else:
                DU_examlist.append(exam)
    for clas in classes:
        for ugi in UserGroupInfo.objects.filter(group=clas):
            for ua in UserAssessment.objects.filter(user = ugi.user, type = 'D'):
                if not ua.at in examlist:
                    examlist.append(ua.at)
                    exam = ga.at
                    exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ga.at, my_usergroupinfo.group)
                    if len(ga.at.get_itcs()) == 1:
                        DS_examlist.append(exam)
                    else:
                        DU_examlist.append(exam)
    
    P_examlist = []
    for ga in GroupAssessment.objects.filter(group = my_usergroupinfo.group, type = 'P'):
        exam = ga.at
        exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ua.at, my_usergroupinfo.group)
        P_examlist.append(exam)
    for clas in classes:
        for ga in GroupAssessment.objects.filter(group = clas, type = 'P'):
            exam = ga.at
            exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ua.at, my_usergroupinfo.group)
            P_examlist.append(exam)
    print P_examlist
    for clas in classes:
        for ugi in UserGroupInfo.objects.filter(group=clas):
            for ua in UserAssessment.objects.filter(user = ugi.user, type = 'P'):
                print ugi.user.email, ua.at.name, ua.at in P_examlist
                if not ua.at in P_examlist:
                    exam = ua.at
                    exam.finished_std_num, exam.std_num, exam.finish_rate = get_finished_std_num(ua.at, my_usergroupinfo.group)
                    P_examlist.append(exam)
                    print P_examlist
     
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'my_info':my_info,
        'my_usergroupinfo':my_usergroupinfo,
        'examlist':examlist,
        'DS_examlist':DS_examlist,
        'DU_examlist':DU_examlist,
        'P_examlist':P_examlist,
    })
    return render_to_response('tch/kice_assess_result.html', variables)

def kice_at_result(request, at_id):
    if request.user.is_authenticated():
        if len(request.user.usergroupinfo_set.filter(group__groupdetail__type='T')) == 0:
            return redirect('/tch/logout')
    else:
        return redirect('/tch/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__groupdetail__type='S')
    
    at = AssessmentTemplate.objects.get(id=at_id)
    
    std_list = []
    finished_std_num = 0
    gas = GroupAssessment.objects.filter(at = at)
    for ga in gas:
        ugis = UserGroupInfo.objects.filter(group = ga.group)
        for ugi in ugis:
            if not ugi.user in std_list:
                std_list.append(ugi.user)
    ugis = UserGroupInfo.objects.filter(group = my_usergroupinfo.group)
    for ugi in ugis:
        uas = UserAssessment.objects.filter(at=at, user=ugi.user)
        if len(uas) != 0 and not ugi.user in std_list:
            std_list.append(ugi.user)
    for std in std_list:
        std.is_finished = False
        uas = UserAssessment.objects.filter(at=at, user=std)
        if len(uas) != 0 and uas[0].end_time != None:
            std.is_finished = True
            finished_std_num+=1
        
    std_num = len(std_list)
    finish_rate = finished_std_num*100/std_num
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
        'at':at,
        'std_list':std_list,
        'finished_std_num':finished_std_num,
        'std_num':std_num,
        'finish_rate':finish_rate,
    })
    return render_to_response('tch/kice_at_result.html', variables)
    