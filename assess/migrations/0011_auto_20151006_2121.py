# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0010_auto_20151006_2018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemtemplate',
            old_name='ict',
            new_name='itc',
        ),
    ]
