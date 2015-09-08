# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0004_mappeditemassessmenttemplate_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassessment',
            name='solving_order_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userassessment',
            name='solving_seconds',
            field=models.IntegerField(null=True),
        ),
    ]
