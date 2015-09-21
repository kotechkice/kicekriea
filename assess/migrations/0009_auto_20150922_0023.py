# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0008_gradeduseritem_item_permutation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userassessment',
            name='ci_id',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
