# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0028_assessmenttemplatelevelhelp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTemplateCategoryLevelHelp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('help_h', models.TextField(null=True)),
                ('help_m', models.TextField(null=True)),
                ('help_l', models.TextField(null=True)),
                ('help_f', models.TextField(null=True)),
                ('itc', models.OneToOneField(to='assess.ItemTemplateCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='assessmenttemplatelevelhelp',
            name='at',
        ),
        migrations.DeleteModel(
            name='AssessmentTemplateLevelHelp',
        ),
    ]
