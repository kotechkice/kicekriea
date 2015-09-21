from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Create your models here.
class AssessmentTemplate(models.Model):
    ct_id = models.IntegerField(null=True)
    based_ct_id = models.IntegerField(null=True)
    
    name = models.CharField(max_length=100)
    order_number = models.PositiveSmallIntegerField(null=True)
    
    creator = models.ForeignKey(User)
    owner_group = models.ForeignKey(Group, null=True)
    
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    modification_time = models.DateTimeField(null=True)
    expiration_time = models.DateTimeField(null=True)
    
    period_start = models.DateTimeField(null=True)
    period_end = models.DateTimeField(null=True)
    
    is_editable = models.BooleanField(default=True)
    is_fixed_item = models.BooleanField(default=False)
    is_random_order = models.BooleanField(default=True)
    is_random_choice_order = models.BooleanField(default=True)
    
    num_item = models.PositiveSmallIntegerField(null=True)
    num_item_template = models.PositiveSmallIntegerField(null=True)
    
    def __unicode__(self):
        return self.name
    
class ItemTemplate(models.Model):
    cafa_it_id = models.IntegerField()
    choices_in_a_row = models.IntegerField(null=True)
    def __unicode__(self):
        return str(self.cafa_it_id)

class MappedItemAssessmentTemplate(models.Model):
    at = models.ForeignKey(AssessmentTemplate)
    it = models.ForeignKey(ItemTemplate)
    order = models.IntegerField(null=True)
    def __unicode__(self):
        return self.at.name + '-' + str(self.it.cafa_it_id)
    
class UserAssessment(models.Model):
    at = models.ForeignKey(AssessmentTemplate)
    user = models.ForeignKey(User)
    ci_id = models.CharField(max_length=80, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    solving_order_num = models.IntegerField(null=True)
    solving_seconds = models.IntegerField(null=True)
    def __unicode__(self):
        return self.at.name + '-' + self.user.email

class GradedUserItem(models.Model):
    ua = models.ForeignKey(UserAssessment)
    it = models.ForeignKey(ItemTemplate)
    order = models.IntegerField(null=True)
    seed = models.IntegerField(null=True)
    permutation = models.CharField(max_length=10, null=True)
    item_permutation = models.CharField(max_length=10, null=True)
    response = models.CharField(max_length=50, null=True)
    correctanswer = models.CharField(max_length=50, null=True)
    elapsed_time = models.IntegerField(null=True)
    def __unicode__(self):
        return self.ua.at.name + ' - ' +self.ua.user.email + ' - ' + str(self.it.cafa_it_id)
    
    