# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userassessment',
            name='ci_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
