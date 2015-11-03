# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0020_itemtemplate_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplatecategory',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
