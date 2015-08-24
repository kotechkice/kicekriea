from django.contrib import admin
from auth_ext.models import *

# Register your models here.
admin.site.register(UserGroupInfo)
admin.site.register(GroupDetail)
admin.site.register(UserDetail)
admin.site.register(GroupAddress)