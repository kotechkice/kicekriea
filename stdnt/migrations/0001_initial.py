# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0003_gradeduseritem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exam_order', models.IntegerField(null=True)),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
            ],
        ),
    ]
