from stdnt.models import *
from django.db.models import F

def set_it_level_from_itnum_str(at, itnum_str, leveltype):
    itnum_list = map(lambda x:int(x), itnum_str.split(','))
    set_it_level_from_itnum_list(at, itnum_list, leveltype)
    
def set_it_level_from_itnum_list(at, itnum_list, leveltype):
    for itnum in itnum_list:
        exist_list = ItemTemplate.objects.filter(cafa_it_id=itnum)
        if len(exist_list) == 0:
            it = ItemTemplate()
            it.cafa_it_id = itnum
            it.save()
        else:
            it = exist_list[0] 
        si = StandardItem()
        si.at = at
        si.level = leveltype
        si.it = it
        si.save()

def assess_user_by_exam(ua):
    ae = AssessEaxm()
    ae.ua = ua
    ae.user = ua.user
        
    all_its = map(lambda x:x.it, ua.gradeduseritem_set.filter(response = F('correctanswer')))
    its = map(lambda x:x.it, StandardItem.objects.filter(at=ua.at, level='L'))
    if len(set(all_its) & set(its)) < 3:
        ae.level = 'F'
        ae.save()
        return True
    its = map(lambda x:x.it, StandardItem.objects.filter(at=ua.at, level='M'))
    if len(set(all_its) & set(its)) < 3:
        ae.level = 'L'
        ae.save()
        return True
    its = map(lambda x:x.it, StandardItem.objects.filter(at=ua.at, level='H'))
    if len(set(all_its) & set(its)) < 3:
        ae.level = 'M'
        ae.save()
        return True
    ae.level = 'H'
    ae.save()
    return True
    
