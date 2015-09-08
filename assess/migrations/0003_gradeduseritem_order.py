# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0002_auto_20150903_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeduseritem',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
