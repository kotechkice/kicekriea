# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0023_auto_20151112_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupassessment',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='groupassessment',
            name='solving_order_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='groupassessment',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
