from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_origin
from django.contrib.auth import logout as logout_origin

from mngins import strings as mngins_string
from home import strings as home_string
from home.funcs import code_str_generator

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
                            data = json.dumps({'status':"success", 'msg':'/mngins'})
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
        return redirect('/mngins')
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
    })
    return render_to_response('mngins/login.html', variables)

def main(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
    })
    return render_to_response('mngins/main.html', variables)

def logout(request):
    logout_origin(request)
    return redirect('/mngins/login')

def modify_auths(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    
    if request.is_ajax() :
        #print request.GET
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
        #print request.GET['method']
        if request.GET['method'] == 'add_new_mng':
            if 'email' in request.GET and 'firstname' in request.GET and 'lastname' in request.GET and 'comnum' in request.GET:
                email = request.GET['email']
                firstname = request.GET['firstname']
                lastname = request.GET['lastname']
                comnum = request.GET['comnum']
                
                group = Group.objects.get(name='1')
                if adduser_createpw_sendmail(email=email, group=group, firstname=firstname, lastname=lastname, group_id=comnum):
                    data = json.dumps({'status':"success"})
                else:
                    data = json.dumps({'status':"fail"})
            else:
                data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'del_mng':
            if 'email' in request.GET:
                email = request.GET['email']
                if del_user(email):
                    data = json.dumps({'status':"success"})
            else:
                data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'send_newpw':
            if not 'email' in request.GET:
                data = json.dumps({'status':"fail"})
            else:
                email = request.GET['email']
                if createpassword_sendmail(email):
                    data = json.dumps({'status':"success"})
                else:
                    data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'add_school':
            if 'school_name' in request.GET and 'school_addr' in request.GET and 'email' in request.GET and 'firstname' in request.GET and 'lastname' in request.GET and 'comnum' in request.GET:
                school_name = request.GET['school_name']
                school_addr = request.GET['school_addr']
                email = request.GET['email']
                firstname = request.GET['firstname']
                lastname = request.GET['lastname']
                comnum = request.GET['comnum']
                if email == '' or school_name == '':
                    data = json.dumps({'status':"fail"})
                elif len(User.objects.filter(email=email)) != 0:
                    data = json.dumps({'status':"fail"})
                elif len(school_addr) > GroupAddress.ADDR_LEN_LIMIT:
                    data = json.dumps({'status':"fail"})
                else:
                    new_school = Group()
                    new_school.name = school_name
                    new_school.save()
                    if adduser_createpw_sendmail(email=email, group=new_school, firstname=firstname, lastname=lastname, group_id=comnum, is_groupsuperuser=True):
                        new_school_detail = GroupDetail()
                        new_school_detail.group = new_school
                        new_school_detail.upper_group = Group.objects.get(name='1')
                        new_school_detail.nickname = school_name
                        new_school_detail.type = 'S'
                        new_school_detail.save()
                        
                        new_school_addr = GroupAddress()
                        new_school_addr.group = new_school
                        new_school_addr.address = school_addr
                        new_school_addr.save()
                        
                        new_school.groupdetail = new_school_detail
                        new_school.groupaddress = new_school_addr
                        new_school.name = str(new_school.id)
                        new_school.save()
                        
                        tg = Group()
                        tg.name = school_name + 't'
                        tg.save()
                        
                        tg.detail = GroupDetail()
                        tg.detail.group = tg
                        tg.detail.uppergroup = new_school
                        tg.detail.nickname = home_string.TEACHER
                        tg.detail.type = 'T'
                        tg.detail.save()
                        
                        tg.name = str(tg.id)
                        tg.save()
                        new_user_group_info = UserGroupInfo()
                        new_user_group_info.user = User.objects.get(email=email)
                        new_user_group_info.group = tg
                        new_user_group_info.save()
                        
                        data = json.dumps({'status':"success"})
                    else:
                        data = json.dumps({'status':"fail"})
        elif request.GET['method'] == 'modify_school_info':
            if 'school_id' in request.GET and 'school_name' in request.GET and 'school_addr' in request.GET:
                school_id = request.GET['school_id']
                school_name = request.GET['school_name']
                school_addr = request.GET['school_addr']
                if len(Group.objects.filter(name=school_id)) == 0 :
                    data = json.dumps({'status':"fail"})
                else:
                    school = Group.objects.get(name=school_id)
                    school.groupdetail.nickname = school_name
                    school.groupdetail.save()
                    school.groupaddress.address = school_addr
                    school.groupaddress.save()
                    data = json.dumps({'status':"success"})
            else:
                data = json.dumps({'status':"fail"})
        else:
            data = json.dumps({'status':"fail"})
            
        return HttpResponse(data, 'application/json')
    
    mngins_members = map(lambda x:x.user, UserGroupInfo.objects.filter(group__name='1', is_groupsuperuser=False))
    for index in range(len(mngins_members)):
        mngins_members[index].comnum = mngins_members[index].usergroupinfo_set.filter(group__name='1')[0].user_id_of_group
        
    schools = Group.objects.filter(groupdetail__type = 'S')
    
    for index in range(len(schools)):
        schools[index].mng = UserGroupInfo.objects.filter(group=schools[index], is_groupsuperuser=True)[0].user
    input_code = code_str_generator(size=4)
    variables = RequestContext(request, {
        'mngins_members' : mngins_members,
        'schools' : schools,
        'input_code' : input_code,
        'mngins_string' : mngins_string,
        'home_string' : home_string,
    })
    return render_to_response('mngins/modify_auths.html', variables) 


def modify_pinfo(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    
    my_info = request.user
    my_usergroupinfo = my_info.usergroupinfo_set.get(group__name=1)
    
    if request.method == 'POST':
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
        else:
            data = json.dumps({'status':"fail"})
        
        return HttpResponse(data, 'application/json')

    comnum = my_usergroupinfo.user_id_of_group
    
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
        'my_info' : my_info,
        'comnum' : comnum
    })
    return render_to_response('mngins/modify_pinfo.html', variables) 

