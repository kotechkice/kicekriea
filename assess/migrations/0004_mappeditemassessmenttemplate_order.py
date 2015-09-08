# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0003_gradeduseritem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappeditemassessmenttemplate',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
