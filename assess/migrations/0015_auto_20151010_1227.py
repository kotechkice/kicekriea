# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0014_auto_20151009_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtemplatecategory',
            name='type',
        ),
        migrations.AddField(
            model_name='itemtemplatecategorylevellabel',
            name='type',
            field=models.CharField(max_length=1, null=True, choices=[(b'N', b'None'), (b'R', b'Root'), (b'U', b'Unit'), (b'G', b'Grade'), (b'M', b'Middle Unit'), (b'D', b'Domain'), (b'C', b'Cluster'), (b'S', b'Standard'), (b'E', b'Etc')]),
        ),
    ]
