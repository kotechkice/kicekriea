# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0009_auto_20150922_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, null=True, choices=[(b'R', b'Root'), (b'U', b'Unit'), (b'G', b'Grade'), (b'D', b'Domain'), (b'C', b'Cluster'), (b'S', b'Standard')])),
                ('name', models.CharField(max_length=80, null=True)),
                ('upper_itc', models.ForeignKey(to='assess.ItemTemplateCategory', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='ict',
            field=models.ForeignKey(to='assess.ItemTemplateCategory', null=True),
        ),
    ]
