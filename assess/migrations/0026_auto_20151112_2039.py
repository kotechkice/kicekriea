# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0025_auto_20151112_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassessment',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userassessment',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
