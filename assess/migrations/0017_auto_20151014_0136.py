# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0016_auto_20151013_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('level', models.IntegerField(null=True)),
                ('upper_atc', models.ForeignKey(to='assess.AssessmentTemplateCategory', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='assessmenttemplate',
            name='atc',
            field=models.ForeignKey(to='assess.AssessmentTemplateCategory', null=True),
        ),
    ]
