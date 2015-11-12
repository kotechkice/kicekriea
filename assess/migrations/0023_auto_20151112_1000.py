# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0022_assessmenttemplate_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupassessment',
            name='type',
            field=models.CharField(max_length=1, null=True, choices=[(b'D', b'Diagnosis'), (b'P', b'Practice')]),
        ),
        migrations.AddField(
            model_name='userassessment',
            name='type',
            field=models.CharField(max_length=1, null=True, choices=[(b'D', b'Diagnosis'), (b'P', b'Practice')]),
        ),
    ]
