# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0012_auto_20151009_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplatecategory',
            name='level_label',
            field=models.ForeignKey(to='assess.ItemTemplateCategoryLevelLabel', null=True),
        ),
        migrations.AlterField(
            model_name='itemtemplatecategorylevellabel',
            name='mark',
            field=models.CharField(max_length=4, null=True, choices=[(b'None', b'It has no type.'), (b'BRPO', b'Big Rome letters with a point'), (b'SRPO', b'Small Rome letters with a point'), (b'NMPO', b'Numbers with a point'), (b'NMAC', b'Numbers in a circle'), (b'NMAR', b'Numbers with a round bracket'), (b'NMRB', b'Numbers in round brackets'), (b'NMSB', b'Numbers in square brackets'), (b'NMBR', b'Numbers in braces')]),
        ),
    ]
