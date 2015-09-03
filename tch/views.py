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
    
    variables = RequestContext(request, {
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
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
                    #new_tch = User.objects.get(email=email)
                    
                    #tg = Group()
                    #tg.name = email + 't'
                    #tg.save()
                    
                    data = json.dumps({'status':"success"})
                else:
                    data = json.dumps({'status':"fail"})
            else:
                data = json.dumps({'status':"fail"})
        else:
            data = json.dumps({'status':"fail"})
        return HttpResponse(data, 'application/json')
    
    tg = request.user.usergroupinfo_set.get(group__groupdetail__type='T').group
    tchs = map(lambda x:x.user, UserGroupInfo.objects.filter(group=tg))
    for index in range(len(tchs)):
        tchs_usergroupinfo =  tchs[index].usergroupinfo_set.get(group__groupdetail__type='S')
        tchs[index].comnum = tchs_usergroupinfo.user_id_of_group
        tchs[index].is_groupsuperuser = tchs_usergroupinfo.is_groupsuperuser
    
    #grades = Group.objects.filter(groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="G")
    classes = Group.objects.filter(groupdetail__upper_group__groupdetail__upper_group=my_usergroupinfo.group, groupdetail__type="C")
        
    input_code = code_str_generator(size=4)
    
    variables = RequestContext(request, {
        'tchs' : tchs,
        'classes' : classes,
        'input_code' : input_code,
        'tch_string' : tch_string,                                 
        'home_string' : home_string,
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