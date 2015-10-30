from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_origin
from django.contrib.auth import logout as logout_origin
from django.db.models import F

from mngins import strings as mngins_string
from home import strings as home_string
from home.funcs import code_str_generator

from auth_ext.models import *
from auth_ext.funcs import * 

from assess.models import *

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

def itemtemp(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
        
    })
    return render_to_response('mngins/itemtemp.html', variables) 

def itemtemp_update(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    if request.is_ajax():
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')
        if request.GET['method'] == 'set_one_item':
            if 'iteminfo' in request.GET:
                iteminfo = json.loads(request.GET['iteminfo'])
                exist_list = ItemTemplate.objects.filter(cafa_it_id=iteminfo['itemID'])
                if len(exist_list) == 0:
                    it = ItemTemplate()
                    it.cafa_it_id = iteminfo['itemID']
                else:
                    it = exist_list[0]
                it.choices_in_a_row = iteminfo['choices_in_a_row'] if iteminfo['choices_in_a_row'].isdigit() else 1
                it.difficulty = iteminfo['difficulty'] if iteminfo['difficulty'].isdigit() else None
                it.answer_type = iteminfo['answer_type'][0] if len(iteminfo['answer_type'])>0 else None
                it.points = iteminfo['points'] if iteminfo['points'].isdigit() else None
                it.year = iteminfo['year'] if iteminfo['year'].isdigit() else None
                it.ability = iteminfo['ability'] if iteminfo['ability'].isdigit() else None
                it.description = iteminfo['description']
                it.exposure = iteminfo['exposure'] if iteminfo['exposure'].isdigit() else None
                it.correct = iteminfo['correct'] if iteminfo['correct'].isdigit() else None
                it.complexity = iteminfo['complexity'] if iteminfo['complexity'].isdigit() else None
                it.institue = iteminfo['institue'] if iteminfo['institue'].isdigit() else None
                it.height = iteminfo['height'] if iteminfo['height'].isdigit() else None
                
                it.save()
                data = json.dumps({'status':"success"})
        return HttpResponse(data, 'application/json')
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
        
    })
    return render_to_response('mngins/itemtemp_update.html', variables) 

def itemtemp_category(request):
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

        if request.GET['method'] == 'set_itemtemp':
            if 'itemid_str' in request.GET:
                #print request.GET['itemid_str'].split()
                for itemid in request.GET['itemid_str'].split():
                    #print itemid
                    exist_list = ItemTemplate.objects.filter(cafa_it_id=itemid)
                    if len(exist_list) == 0:
                        it = ItemTemplate()
                        it.cafa_it_id = itemid
                        it.save()
                no_category_itemids = map(lambda x:x.cafa_it_id, ItemTemplate.objects.filter(itc=None))
                
                data = json.dumps({'status':"success", 'no_category_itemids':no_category_itemids})
        if request.GET['method'] == 'sel_itc':
            if 'itc_id' in request.GET and 'level' in request.GET:
                if request.GET['itc_id'] == 'all':
                    pass
                elif request.GET['itc_id'] == 'none':
                    pass
                else:
                    label_level = request.GET['level']
                    next_levels = ItemTemplateCategoryLevelLabel.objects.filter(level = int(label_level)+1)
                    next_level_label = {'name':'', 'type':'N', 'mark':'None'}
                    if len(next_levels) != 0:
                        next_level_label['name'] = next_levels[0].name
                        next_level_label['type'] = next_levels[0].type
                        next_level_label['mark'] = next_levels[0].mark
                    
                    itc_objs = ItemTemplateCategory.objects.filter(upper_itc__id=request.GET['itc_id']).order_by('order')
                    itcs = []
                    
                    mitcs = MappedItemTemplateCategory.objects.filter(itc__id = request.GET['itc_id'])
                    itids_in_itc = map(lambda x:x.it.cafa_it_id, mitcs)
                    
                    for itc_obj in itc_objs:
                        itcs.append({'id':itc_obj.id, 'name':itc_obj.name})
                    data = json.dumps({
                        'status':"success", 
                        'next_level_label':next_level_label, 
                        'itcs':itcs,
                        'itids_in_itc':itids_in_itc,
                    })
                    #data = json.dumps({'status':"success"})
        if request.GET['method'] == 'change_category_type':
            if 'type' in request.GET and 'level' in request.GET and 'name' in request.GET:
                itclls = ItemTemplateCategoryLevelLabel.objects.filter(level = request.GET['level'])
                if len(itclls) != 0:
                    itcll = itclls[0]
                    itcll.type = request.GET['type']
                    itcll.name = request.GET['name']
                    itcll.save()
                    data = json.dumps({
                        'status':"success", 
                        'type':itcll.type
                    })
        if request.GET['method'] == 'change_category_mark':
            if 'mark' in request.GET and 'level' in request.GET:
                itclls = ItemTemplateCategoryLevelLabel.objects.filter(level = request.GET['level'])
                if len(itclls) != 0:
                    itcll = itclls[0]
                    itcll.mark = request.GET['mark']
                    itcll.save()
                    data = json.dumps({
                        'status':"success", 
                        'mark':itcll.mark
                    })
        if request.GET['method'] == 'add_category':
            if 'level' in request.GET and 'name' in request.GET and 'upper_itc_id' in request.GET:
                level = int(request.GET['level'])
                new_itc = ItemTemplateCategory()
                if level != 0:
                    upper_itcs = ItemTemplateCategory.objects.filter(id=request.GET['upper_itc_id'])
                    if len(upper_itcs) != 0:
                        upper_itc = upper_itcs[0]
                        new_itc.upper_itc = upper_itc
                else:
                    upper_itc = None
                new_itc.name = request.GET['name']
                itclls = ItemTemplateCategoryLevelLabel.objects.filter(level = level)
                if len(itclls) != 0:
                    new_itc.level_label = itclls[0]
                itc_objs = ItemTemplateCategory.objects.filter(upper_itc = upper_itc)
                new_itc.order = len(itc_objs)+1
                new_itc.save()
                itc_objs = ItemTemplateCategory.objects.filter(upper_itc = upper_itc).order_by('order')
                itc_lists = []
                for itc_obj in itc_objs:
                    itc_lists.append({'id':itc_obj.id, 'name':itc_obj.name, 'order':itc_obj.order})
                json.dumps(itc_lists)
                data = json.dumps({
                    'status':"success",
                    'itc_lists':itc_lists
                })
        if request.GET['method'] == 'modify_category':
            if 'id' in request.GET and 'name' in request.GET and 'level' in request.GET and 'upper_itc_id' in request.GET:
                itcs = ItemTemplateCategory.objects.filter(id=request.GET['id'])
                if len(itcs) != 0:
                    itc = itcs[0]
                    itc.name = request.GET['name']
                    itc.save()
                    
                    level = int(request.GET['level'])
                    upper_itc = None
                    if level != 0:
                        upper_itcs = ItemTemplateCategory.objects.filter(id=request.GET['upper_itc_id'])
                        if len(upper_itcs) != 0:
                            upper_itc = upper_itcs[0]
                    itc_objs = ItemTemplateCategory.objects.filter(upper_itc = upper_itc).order_by('order')
                    itc_lists = []
                    for itc_obj in itc_objs:
                        itc_lists.append({'id':itc_obj.id, 'name':itc_obj.name, 'order':itc_obj.order})
                    json.dumps(itc_lists)
                    data = json.dumps({
                        'status':"success",
                        'itc_lists':itc_lists
                    })
        if request.GET['method'] == 'del_category':
            def del_category(itc):
                daughters = ItemTemplateCategory.objects.filter(upper_itc=itc)
                for daughter in daughters:
                    del_category(daughter)
                
                younger_sisters = ItemTemplateCategory.objects.filter(upper_itc=itc.upper_itc, order__gt = itc.order)
                younger_sisters.update(order = F('order') -1 )
                itc.delete()
                
            if 'id' in request.GET and 'level' in request.GET and 'upper_itc_id' in request.GET:
                itcs = ItemTemplateCategory.objects.filter(id=request.GET['id'])
                if len(itcs) != 0:
                    itc = itcs[0]
                    if itc.level_label.level == 0 and itc.order==1:
                        pass
                    elif itc.level_label.level == 0 and itc.order==2:
                        pass
                    else:
                        del_category(itc)
                    
                    level = int(request.GET['level'])
                    upper_itc = None
                    if level != 0:
                        upper_itcs = ItemTemplateCategory.objects.filter(id=request.GET['upper_itc_id'])
                        if len(upper_itcs) != 0:
                            upper_itc = upper_itcs[0]
                    itc_objs = ItemTemplateCategory.objects.filter(upper_itc = upper_itc).order_by('order')
                    itc_lists = []
                    for itc_obj in itc_objs:
                        itc_lists.append({'id':itc_obj.id, 'name':itc_obj.name, 'order':itc_obj.order})
                    json.dumps(itc_lists)
                    data = json.dumps({
                        'status':"success",
                        'itc_lists':itc_lists
                    })
        if request.GET['method'] == 'get_or_create_levellabel':
            if 'level' in request.GET:
                itclls = ItemTemplateCategoryLevelLabel.objects.filter(level = request.GET['level'])
                if len(itclls) != 0:
                    itcll = itclls[0]
                else:
                    itcll = ItemTemplateCategoryLevelLabel()
                    itcll.type = 'N'
                    itcll.mark = 'None'
                    itcll.save()
                data = json.dumps({
                    'status':"success", 
                    'mark':itcll.mark,
                    'type':itcll.type
                })
                
        if request.GET['method'] == 'change_order':
            if ('id' and 'direction' and 'level' and 'upper_itc_id') in request.GET:
                itc = ItemTemplateCategory.objects.get(id=request.GET['id'])
                level = int(request.GET['level'])
                
                upper_itc = None
                if level != 0:
                    upper_itcs = ItemTemplateCategory.objects.filter(id=request.GET['upper_itc_id'])
                    if len(upper_itcs) != 0:
                        upper_itc = upper_itcs[0]
                        
                if request.GET['direction'] == 'up':
                    if itc.order > 1:
                        conceding_itc = ItemTemplateCategory.objects.get(upper_itc = upper_itc, order=itc.order-1)
                        itc.order -= 1
                        conceding_itc.order += 1
                        itc.save()
                        conceding_itc.save()
                else: # down
                    if len(ItemTemplateCategory.objects.filter(upper_itc = upper_itc, order=itc.order+1)) == 1:
                        conceding_itc = ItemTemplateCategory.objects.get(upper_itc = upper_itc, order=itc.order+1)
                        conceding_itc.order -= 1
                        itc.order += 1
                        itc.save()
                        conceding_itc.save()
                changed_order = itc.order
                itc_objs = ItemTemplateCategory.objects.filter(upper_itc = upper_itc).order_by('order')
                itc_lists = []
                for itc_obj in itc_objs:
                    itc_lists.append({'id':itc_obj.id, 'name':itc_obj.name, 'order':itc_obj.order})
                json.dumps(itc_lists)
                data = json.dumps({
                    'status':"success",
                    'itc_lists':itc_lists,
                    'changed_order':changed_order
                })
        return HttpResponse(data, 'application/json')
    
    mitcs = MappedItemTemplateCategory.objects.all()
    itids_in_itc = map(lambda x:x.it.cafa_it_id, mitcs)
    no_cate_its = ItemTemplate.objects.exclude(cafa_it_id__in = itids_in_itc)

    itcll0_s = ItemTemplateCategoryLevelLabel.objects.get(level=0)
    itc0_s = ItemTemplateCategory.objects.filter(level_label = itcll0_s).order_by('order')
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
        'no_cate_its':no_cate_its,
        'itcll0_s' : itcll0_s,
        'itc0_s' : itc0_s,
        
    })
    return render_to_response('mngins/itemtemp_category.html', variables) 

def assesstemp(request):
    if request.user.is_authenticated():
        if len(UserGroupInfo.objects.filter(group__name='1', user=request.user)) == 0:
            return redirect('/mngins/logout')
    else:
        return redirect('/mngins/login')
    
    if request.is_ajax() :
        data = json.dumps({'status':"fail"})
        if not 'method' in request.GET:
            data = json.dumps({'status':"fail"})
            return HttpResponse(data, 'application/json')

        if request.GET['method'] == 'sel_atc':
            if 'atc_id' in request.GET and 'level' in request.GET:
                if request.GET['atc_id'] == 'all':
                    pass
                elif request.GET['atc_id'] == 'none':
                    pass
                else:
                    atc_objs = AssessmentTemplateCategory.objects.filter(upper_atc__id=request.GET['atc_id'])
                    atcs = []
                    for atc_obj in atc_objs:
                        atcs.append({'id':atc_obj.id, 'name':atc_obj.name})
                    data = json.dumps({'status':"success", 'atcs':atcs})
            
        return HttpResponse(data, 'application/json')
    
    
    atc0_s =  AssessmentTemplateCategory.objects.filter(level=0)
    
    variables = RequestContext(request, {
        'mngins_string' : mngins_string,
        'home_string' : home_string,
        'atc0_s':atc0_s,
    })
    return render_to_response('mngins/assesstemp.html', variables) 
