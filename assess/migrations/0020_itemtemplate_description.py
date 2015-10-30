# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0019_auto_20151029_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplate',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
