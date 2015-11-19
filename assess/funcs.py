from assess.models import *
from django.utils import timezone
'''
def create_ua_from_at(at, user, ci_id, type, start, end):
    ua = UserAssessment()
    ua.user = user
    ua.at = at
    ua.type = type
    ua.period_start = start
    ua.period_end = end
    ua.save()
''' 
    
def create_ua_from_itemdict_N_at(at, itemdict, user, ci_id):
    ua = UserAssessment()
    ua.at = at
    ua.user = user
    ua.ci_id = ci_id 
    ua.start_time = timezone.now()
    ua.solving_order_num = 1
    ua.solving_seconds = 0
    ua.save()
    for index in range(1, len(itemdict)+1):
        #print itemdict[str(index)]
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
        it.choices_in_a_row = itemdict[str(index)]['NumChoices']
        it.save()
        gui.order = index
        gui.seed = int(itemdict[str(index)]['Seed'])
        gui.permutation = ''.join(itemdict[str(index)]['Permutation'].split(',')) 
        gui.response = 'x'
        gui.correctanswer = 'x'
        gui.elapsed_time = 0
        gui.save()
    return ua.id

def set_item_permutation_in_gui(gui, item_permutation_str):
    gui.item_permutation = ''.join(item_permutation_str.split(',')) 
    gui.save()
    return True

def create_its_from_itnum_str_N_at(at, itnum_str):
    itnum_list = map(lambda x:int(x), itnum_str.split(','))
    create_its_from_itnum_list_N_at(at, itnum_list)
    
def create_its_from_itnum_list_N_at(at, itnum_list):
    order = 1
    #print itnum_list
    for itnum in itnum_list:
        #print itnum
        exist_list = ItemTemplate.objects.filter(cafa_it_id=itnum)
        if len(exist_list) == 0:
            it = ItemTemplate()
            it.cafa_it_id = itnum
            it.save()
        else:
            it = exist_list[0] 
        miat = MappedItemAssessmentTemplate()
        miat.at = at
        miat.it = it
        miat.order = order
        miat.save()
        order = order + 1