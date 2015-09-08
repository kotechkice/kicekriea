# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0007_gradeduseritem_permutation'),
        ('stdnt', '0002_auto_20150906_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standarditem',
            name='at',
        ),
        migrations.AddField(
            model_name='standarditem',
            name='ua',
            field=models.ForeignKey(default='1', to='assess.UserAssessment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assesseaxm',
            name='level',
            field=models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'Middle'), (b'L', b'Low'), (b'F', b'Fail')]),
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='level',
            field=models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'Middle'), (b'L', b'Low'), (b'F', b'Fail')]),
        ),
    ]
