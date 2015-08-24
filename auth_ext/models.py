from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class UserGroupInfo(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_groupsuperuser =  models.BooleanField(default=False)
    user_id_of_group = models.CharField(max_length=30, null=True)
    
    def __unicode__(self):
        return self.user.username + '-' + self.group.groupdetail.nickname + '(' + self.group.name + ')'
    
class GroupDetail(models.Model):
    GroupTypes = (
        ('M', 'Manager Institution'),
        ('S', 'School'),
        ('T', 'Teacher'),
        ('G', 'Grade'),
        ('C', 'Class')
    )
    group = models.OneToOneField(Group)
    upper_group = models.ForeignKey(Group, null=True, related_name='upper_group')
    nickname = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=GroupTypes)
    
    def __unicode__(self):
        return self.nickname

class GroupAddress(models.Model):
    ADDR_LEN_LIMIT = 1000
    
    group = models.OneToOneField(Group)
    address = models.TextField(null=True)
    
    def clean(self):
        if len(self.address) > self.ADDR_LEN_LIMIT:
            raise ValidationError('The %s length limit is %d bit.' % ('address text', self.ADDR_LEN_LIMIT))
    def __unicode__(self):
        return self.address
    
class UserDetail(models.Model):
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.full_name