from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Create your models here.

class AssessmentTemplateCategory(models.Model):
    name = models.CharField(max_length=80, null=True)
    level = models.IntegerField(null=True)
    upper_atc = models.ForeignKey('self', null=True)
    
    def __unicode__(self):
        return self.name
    
class AssessmentTemplate(models.Model):
    Types = (
        ('D', 'Diagnosis'),
        ('P', 'Practice'),
    )
    type = models.CharField(max_length=1, choices=Types, null=True)
    
    atc = models.ForeignKey(AssessmentTemplateCategory, null=True)
    
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

class ItemTemplateCategoryLevelLabel(models.Model):
    MarkTyeps = (
        ('None', 'It has no type.'),
        ('BRPO', 'Big Rome letters with a point'), # I., II., 'III.
        ('SRPO', 'Small Rome letters with a point'),
        
        ('NMPO', 'Numbers with a point'),
        ('NMAC', 'Numbers in a circle'),
        ('NMAR', 'Numbers with a round bracket'),
        ('NMRB', 'Numbers in round brackets'),
        ('NMSB', 'Numbers in square brackets'),
        ('NMBR', 'Numbers in braces'),
    )
    LevelTypes = (
        ('N', 'None'),
        ('R', 'Root'),
        ('O', 'Course'),
        ('U', 'Unit'),
        ('A', 'Academy'),
        ('G', 'Grade'),
        ('M', 'Middle Unit'),
        ('D', 'Domain'),
        ('C', 'Cluster'),
        ('S', 'Standard'),
        ('E', 'Etc'),
    )
    name = models.CharField(max_length=40, null=True)
    mark = models.CharField(max_length=4, choices=MarkTyeps, null=True)
    level = models.IntegerField(null=True)
    type = models.CharField(max_length=1, choices=LevelTypes, null=True)
    def __unicode__(self):
        return unicode(self.name) or u''

class ItemTemplateCategory(models.Model):
    name = models.CharField(max_length=80, null=True)
    level_label = models.ForeignKey(ItemTemplateCategoryLevelLabel, null=True)
    upper_itc = models.ForeignKey('self', null=True)
    order = models.IntegerField(null=True)
    description = models.TextField(null=True)
    
    def __unicode__(self):
        return unicode(self.name) or u''
  
  
class ItemTemplate(models.Model):
    AnswerTypes = (
        ('N', 'Natural'),
        ('I', 'Integer'),
        ('D', 'Decimal'),
        ('F', 'Fraction'),
        ('E', 'Expression'),
        ('W', 'Word'),
        ('C', "Can't be SPR"),
    )
    cafa_it_id = models.IntegerField()
    difficulty = models.IntegerField(null=True)
    answer_type = models.CharField(max_length=1, choices=AnswerTypes, null=True)
    points = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    ability = models.IntegerField(null=True)
    description = models.TextField(null=True)
    exposure = models.IntegerField(null=True)
    correct = models.IntegerField(null=True)
    complexity = models.IntegerField(null=True)
    institue = models.IntegerField(null=True)
    choices_in_a_row = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    #itc = models.ForeignKey(ItemTemplateCategory, null=True)
    def __unicode__(self):
        return str(self.cafa_it_id)

class MappedItemTemplateCategory(models.Model):
    itc = models.ForeignKey(ItemTemplateCategory)
    it = models.ForeignKey(ItemTemplate)
    def __unicode__(self):
        return str(self.it.cafa_it_id) + '-' + self.itc.name
  
class MappedItemAssessmentTemplate(models.Model):
    at = models.ForeignKey(AssessmentTemplate)
    it = models.ForeignKey(ItemTemplate)
    order = models.IntegerField(null=True)
    def __unicode__(self):
        return self.at.name + '-' + str(self.it.cafa_it_id)

class GroupAssessment(models.Model):
    at = models.ForeignKey(AssessmentTemplate)
    group = models.ForeignKey(Group)
    #creator = models.ForeignKey(User)
    #creation_time = models.DateTimeField(null=True)

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
    
    