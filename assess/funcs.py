from assess.models import *
from django.utils import timezone

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
        print itemdict[str(index)]
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

def create_its_from_itnum_str_N_at(at, itnum_str):
    #mat = MappedItemAssessmentTemplate()
    #print 'create_it_str_in_at'
    #print at.name
    #print itnum_str
    itnum_list = map(lambda x:int(x), itnum_str.split(','))
    create_itnum_list_in_at(at, itnum_list)
    
def create_its_from_itnum_list_N_at(at, itnum_list):
    for itnum in itnum_list:
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
        miat.save()