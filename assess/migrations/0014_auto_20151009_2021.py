# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0013_auto_20151009_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtemplatecategory',
            name='level',
        ),
        migrations.AddField(
            model_name='itemtemplatecategorylevellabel',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
