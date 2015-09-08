# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0005_auto_20150904_2137'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stdnt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessEaxm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'High'), (b'L', b'High'), (b'F', b'Fail')])),
                ('ua', models.ForeignKey(to='assess.UserAssessment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StandardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'H', b'High'), (b'M', b'High'), (b'L', b'High'), (b'F', b'Fail')])),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
                ('it', models.ForeignKey(to='assess.ItemTemplate')),
            ],
        ),
        migrations.AddField(
            model_name='examlist',
            name='context',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examlist',
            name='help_f',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examlist',
            name='help_h',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examlist',
            name='help_l',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examlist',
            name='help_m',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examlist',
            name='standard',
            field=models.CharField(default=datetime.datetime(2015, 9, 6, 14, 10, 33, 808453, tzinfo=utc), max_length=25),
            preserve_default=False,
        ),
    ]
