from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

from auth_ext.models import *
from auth_ext.strings import *

from home.funcs import code_str_generator

def createpassword_sendmail(email, password_size=4):
    if len(User.objects.filter(email=email)) == 0:
        return False
    if password_size <= 0:
        return False
    user = User.objects.get(email=email)
    
    #pw = code_str_generator(size=password_size)
    pw= '0000' #fix me, tentative settlement
     
    user.set_password(pw)
    user.save()
    subj_msg = MAIL_MSG_SUBJECT_CREATE_PW
    contents_msg = MAIL_MSG_CONTENTS_CREATE_PW + pw
    
    mng_group = Group.objects.get(name='1')
    mng_master = UserGroupInfo.objects.get(group = mng_group, is_groupsuperuser = True).user
    try:
        send_mail(subj_msg, contents_msg, mng_master.email, [email], fail_silently=True)
    except:
        print "error in send_mail"
    return True


def adduser_createpw_sendmail(email, group, firstname, lastname, group_id, is_groupsuperuser=False):
    if email == '':
        return False
    elif len(User.objects.filter(email=email)) != 0:
        return False
    new_user = User()
    new_user.username = email.split('@')[0]
    new_user.email = email
    new_user.first_name = firstname
    new_user.last_name = lastname
    new_user.set_password('dummy_password')
    new_user.save()
    
    new_user_detail = UserDetail()
    new_user_detail.user = new_user
    new_user_detail.full_name = lastname+firstname
    new_user_detail.save()
    
    new_user.userdetail = new_user_detail
    new_user.username = str(new_user.id)
    new_user.save()
    
    new_user_group_info = UserGroupInfo()
    new_user_group_info.user = new_user
    new_user_group_info.group = group
    new_user_group_info.is_groupsuperuser = is_groupsuperuser
    new_user_group_info.user_id_of_group = group_id
    new_user_group_info.save()
    
    if not createpassword_sendmail(email):
        return False
    
    return True

def del_user(email):
    if len(User.objects.filter(email=email)) == 0:
        return False
    user = User.objects.get(email=email)
    user.usergroupinfo_set.all().delete()
    user.userdetail.delete()
    user.delete()
    return True

def create_class_in_school(school_group, grade_name, class_name):
    gd_list = GroupDetail.objects.filter(upper_group=school_group, type='G', nickname=grade_name)
    if len(gd_list) == 0:
        g = Group()
        g.name = grade_name
        g.save()
        g.groupdetail = GroupDetail()
        g.groupdetail.group = g
        g.groupdetail.type = 'G'
        g.groupdetail.nickname = grade_name
        g.groupdetail.upper_group = school_group
        g.groupdetail.save()
        g.name = str(g.id)
        g.save()
        grade_group = g
    else:
        grade_group = gd_list[0].group
    gd_list = GroupDetail.objects.filter(upper_group=grade_group, type='C', nickname=class_name)
    if len(gd_list) != 0:
        return False
    g = Group()
    g.name = class_name
    g.save()
    g.groupdetail = GroupDetail()
    g.groupdetail.group = g
    g.groupdetail.type = 'C'
    g.groupdetail.nickname = class_name
    g.groupdetail.upper_group = grade_group
    g.groupdetail.save()
    g.name = str(g.id)
    g.save()
        
    return True

def change_class_in_school(clas, school_group, grade_name, class_name):
    gd_list = GroupDetail.objects.filter(upper_group=school_group, type='G', nickname=grade_name)
    if len(gd_list) == 0:
        g = Group()
        g.name = grade_name
        g.save()
        g.groupdetail = GroupDetail()
        g.groupdetail.group = g
        g.groupdetail.type = 'G'
        g.groupdetail.nickname = grade_name
        g.groupdetail.upper_group = school_group
        g.groupdetail.save()
        g.name = str(g.id)
        g.save()
        grade_group = g
    else:
        grade_group = gd_list[0].group
    clas.groupdetail.nickname = class_name
    clas.groupdetail.upper_group = grade_group
    clas.groupdetail.save()
    clas.save()
    return True



