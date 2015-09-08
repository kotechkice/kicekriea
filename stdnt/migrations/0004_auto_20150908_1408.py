# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0007_gradeduseritem_permutation'),
        ('stdnt', '0003_auto_20150908_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standarditem',
            name='ua',
        ),
        migrations.AddField(
            model_name='standarditem',
            name='at',
            field=models.ForeignKey(default='1', to='assess.AssessmentTemplate'),
            preserve_default=False,
        ),
    ]
