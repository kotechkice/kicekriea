from django.contrib import admin
from assess.models import *

# Register your models here.
admin.site.register(AssessmentTemplate)
admin.site.register(ItemTemplate)
admin.site.register(MappedItemAssessmentTemplate)
admin.site.register(UserAssessment)
admin.site.register(GradedUserItem)
