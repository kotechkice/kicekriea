from django.contrib import admin
from assess.models import *

# Register your models here.
admin.site.register(AssessmentTemplateCategory)
admin.site.register(AssessmentTemplate)
admin.site.register(ItemTemplate)
admin.site.register(MappedItemTemplateCategory)

admin.site.register(MappedItemAssessmentTemplate)
admin.site.register(ItemTemplateCategory)
admin.site.register(ItemTemplateCategoryLevelHelp)
admin.site.register(ItemTemplateCategoryLevelLabel)

admin.site.register(GroupAssessment)
admin.site.register(UserAssessment)
admin.site.register(GradedUserItem)
