# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0005_auto_20150904_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplate',
            name='choices_in_a_row',
            field=models.IntegerField(null=True),
        ),
    ]
