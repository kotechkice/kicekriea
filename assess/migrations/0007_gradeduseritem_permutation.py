# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0006_itemtemplate_choices_in_a_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeduseritem',
            name='permutation',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
