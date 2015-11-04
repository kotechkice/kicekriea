# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0021_itemtemplatecategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmenttemplate',
            name='type',
            field=models.CharField(max_length=1, null=True, choices=[(b'D', b'Diagnosis'), (b'P', b'Practice')]),
        ),
    ]
