from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_origin
from django.contrib.auth import logout as logout_origin

from stdnt import strings as stdnt_string
from home import strings as home_string

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
    
    variables = RequestContext(request, {
        'home_string' : home_string,
        'stdnt_string':stdnt_string,
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