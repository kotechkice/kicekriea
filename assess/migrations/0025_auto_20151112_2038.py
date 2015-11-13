# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0024_auto_20151112_1019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupassessment',
            old_name='end_time',
            new_name='period_end',
        ),
        migrations.RenameField(
            model_name='groupassessment',
            old_name='start_time',
            new_name='period_start',
        ),
        migrations.RenameField(
            model_name='userassessment',
            old_name='end_time',
            new_name='period_end',
        ),
        migrations.RenameField(
            model_name='userassessment',
            old_name='start_time',
            new_name='period_start',
        ),
    ]
