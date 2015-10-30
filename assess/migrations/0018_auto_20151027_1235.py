# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('assess', '0017_auto_20151014_0136'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.AddField(
            model_name='itemtemplatecategory',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
