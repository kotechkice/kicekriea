# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0018_auto_20151027_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplate',
            name='ability',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='answer_type',
            field=models.CharField(max_length=1, null=True, choices=[(b'N', b'Natural'), (b'I', b'Integer'), (b'D', b'Decimal'), (b'F', b'Fraction'), (b'E', b'Expression'), (b'W', b'Word'), (b'C', b"Can't be SPR")]),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='complexity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='correct',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='difficulty',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='exposure',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='institue',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='points',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='itemtemplatecategorylevellabel',
            name='type',
            field=models.CharField(max_length=1, null=True, choices=[(b'N', b'None'), (b'R', b'Root'), (b'O', b'Course'), (b'U', b'Unit'), (b'A', b'Academy'), (b'G', b'Grade'), (b'M', b'Middle Unit'), (b'D', b'Domain'), (b'C', b'Cluster'), (b'S', b'Standard'), (b'E', b'Etc')]),
        ),
    ]
