# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0007_gradeduseritem_permutation'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeduseritem',
            name='item_permutation',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
