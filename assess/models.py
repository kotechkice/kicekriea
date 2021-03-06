from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models import F

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
    
    def get_itcs(self):
        its = map(lambda x:x.it, self.mappeditemassessmenttemplate_set.all())
        itcs = []
        for it in its:
            mitcs = it.mappeditemtemplatecategory_set.all()
            for mitc in mitcs:
                if not mitc.itc in itcs:
                    itcs.append(mitc.itc)
        return itcs

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

class ItemTemplateCategoryLevelHelp(models.Model):
    itc = models.OneToOneField(ItemTemplateCategory)
    
    help_h = models.TextField(null=True)
    help_m = models.TextField(null=True)
    help_l = models.TextField(null=True)
    help_f = models.TextField(null=True)
    
  
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
    difficulty = models.IntegerField(null=True) #1: Easy, 2: Intermediate, 3: Hard
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
    Types = (
        ('D', 'Diagnosis'),
        ('P', 'Practice'),
    )
    type = models.CharField(max_length=1, choices=Types, null=True)
    
    at = models.ForeignKey(AssessmentTemplate)
    group = models.ForeignKey(Group)
    
    period_start = models.DateTimeField(null=True)
    period_end = models.DateTimeField(null=True)
    
    solving_order_num = models.IntegerField(null=True)
    def __unicode__(self):
        return self.at.name + '-' + self.group.groupdetail.nickname

class UserAssessment(models.Model):
    Types = (
        ('D', 'Diagnosis'),
        ('P', 'Practice'),
    )
    type = models.CharField(max_length=1, choices=Types, null=True)
    
    at = models.ForeignKey(AssessmentTemplate)
    user = models.ForeignKey(User)
    ci_id = models.CharField(max_length=80, null=True)

    period_start = models.DateTimeField(null=True)
    period_end = models.DateTimeField(null=True)
    
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    
    solving_order_num = models.IntegerField(null=True)
    solving_seconds = models.IntegerField(null=True)
    LevelTypes = (
        ('F','Fail'),
        ('E','Easy'),
        ('I','Intermediate'),
        ('H','Hard'),
        ('N','Unknown'),
    )
    level = models.CharField(max_length=1, choices=LevelTypes, null=True)
    
    def __unicode__(self):
        return self.at.name + '-' + self.user.email
    
    def assess_level(self):
        all_its = map(lambda x:x.it, self.gradeduseritem_set.filter(response = F('correctanswer')))
        level_its = map(lambda x:x.it, self.gradeduseritem_set.filter(it__difficulty=1)) #Easy
        if len(level_its) > 0 and len(set(all_its) & set(level_its))/float(len(set(level_its))) < 2/3.0:
            self.level = 'F'
            self.save()
            return True
        if len(level_its) > 0 and len(set(all_its) & set(level_its))/float(len(set(level_its))) >= 2/3.0:
            self.level = 'E'
            self.save()
            return True
        level_its = map(lambda x:x.it, self.gradeduseritem_set.filter(it__difficulty=2)) #Intermediate
        if len(level_its) > 0 and len(set(all_its) & set(level_its))/float(len(set(level_its))) >= 2/3.0:
            self.level = 'I'
            self.save()
            return True
        level_its = map(lambda x:x.it, self.gradeduseritem_set.filter(it__difficulty=3)) #Hard
        if len(level_its) > 0 and len(set(all_its) & set(level_its))/float(len(set(level_its))) >= 2/3.0:
            self.level = 'H'
            self.save()
            return True
        self.level = 'N'
        self.save()
        return True
    def percent_point_all(self):
        correct_num = len(self.gradeduseritem_set.filter(response = F('correctanswer')))
        all_item_num = len(self.gradeduseritem_set.all())
        return correct_num/float(all_item_num)
    
    def percent_point_itc(self, itc):
        itc_its = map(lambda x:x.it, MappedItemTemplateCategory.objects.filter(itc = itc))
        correct_its = map(lambda x:x.it, self.gradeduseritem_set.filter(response = F('correctanswer')))
        all_its = map(lambda x:x.it, self.gradeduseritem_set.all())
        return len(set(itc_its)&set(correct_its))/float(len(set(itc_its)&set(all_its)))
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
    
    