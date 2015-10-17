# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0011_auto_20151006_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTemplateCategoryLevelLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, null=True)),
                ('mark', models.CharField(max_length=4, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemtemplatecategory',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
