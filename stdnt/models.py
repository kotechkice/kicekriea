from django.db import models
from assess.models import *

# Create your models here.
class ExamList(models.Model):
    at = models.ForeignKey(AssessmentTemplate)
    exam_order = models.IntegerField(null=True)
    
    standard = models.CharField(max_length=25)
    context = models.TextField(null=True)
    
    help_h = models.TextField(null=True)
    help_m = models.TextField(null=True)
    help_l = models.TextField(null=True)
    help_f = models.TextField(null=True)
    
    def __unicode__(self):
        return str(self.exam_order) + ' - '  + self.standard +' - ' + self.at.name
    

class AssessEaxm(models.Model):
    LevelTypes = (
        ('H', 'High'),
        ('M', 'Middle'),
        ('L', 'Low'),
        ('F', 'Fail'),
    )
    user = models.ForeignKey(User)
    ua = models.ForeignKey(UserAssessment)
    level = models.CharField(max_length=1, choices=LevelTypes)
    
    def __unicode__(self):
        return self.user.email + ' - ' + self.level

class StandardItem(models.Model):
    LevelTypes = (
        ('H', 'High'),
        ('M', 'Middle'),
        ('L', 'Low'),
        ('F', 'Fail'),
    )
    at = models.ForeignKey(AssessmentTemplate)
    it = models.ForeignKey(ItemTemplate)
    level = models.CharField(max_length=1, choices=LevelTypes)
    
    def __unicode__(self):
        return self.at.name + ' - ' + str(self.it.cafa_it_id) + ' - ' + self.level
    