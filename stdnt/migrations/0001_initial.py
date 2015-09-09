# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assess', '0007_gradeduseritem_permutation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessEaxm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'Middle'), (b'L', b'Low'), (b'F', b'Fail')])),
                ('ua', models.ForeignKey(to='assess.UserAssessment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExamList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exam_order', models.IntegerField(null=True)),
                ('standard', models.CharField(max_length=25, null=True)),
                ('context', models.TextField(null=True)),
                ('help_h', models.TextField(null=True)),
                ('help_m', models.TextField(null=True)),
                ('help_l', models.TextField(null=True)),
                ('help_f', models.TextField(null=True)),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='StandardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'Middle'), (b'L', b'Low'), (b'F', b'Fail')])),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
                ('it', models.ForeignKey(to='assess.ItemTemplate')),
            ],
        ),
    ]
