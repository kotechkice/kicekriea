# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0015_auto_20151010_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='MappedItemTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='itemtemplate',
            name='itc',
        ),
        migrations.AddField(
            model_name='mappeditemtemplatecategory',
            name='it',
            field=models.ForeignKey(to='assess.ItemTemplate'),
        ),
        migrations.AddField(
            model_name='mappeditemtemplatecategory',
            name='itc',
            field=models.ForeignKey(to='assess.ItemTemplateCategory'),
        ),
    ]
