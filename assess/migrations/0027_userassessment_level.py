# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0026_auto_20151112_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassessment',
            name='level',
            field=models.CharField(max_length=1, null=True, choices=[(b'F', b'Fail'), (b'E', b'Easy'), (b'I', b'Intermediate'), (b'H', b'Hard'), (b'N', b'Unknown')]),
        ),
    ]
