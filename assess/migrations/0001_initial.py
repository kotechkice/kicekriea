# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ct_id', models.IntegerField(null=True)),
                ('based_ct_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('order_number', models.PositiveSmallIntegerField(null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('modification_time', models.DateTimeField(null=True)),
                ('expiration_time', models.DateTimeField(null=True)),
                ('period_start', models.DateTimeField(null=True)),
                ('period_end', models.DateTimeField(null=True)),
                ('is_editable', models.BooleanField(default=True)),
                ('is_fixed_item', models.BooleanField(default=False)),
                ('is_random_order', models.BooleanField(default=True)),
                ('is_random_choice_order', models.BooleanField(default=True)),
                ('num_item', models.PositiveSmallIntegerField(null=True)),
                ('num_item_template', models.PositiveSmallIntegerField(null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('owner_group', models.ForeignKey(to='auth.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradedUserItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seed', models.IntegerField(null=True)),
                ('response', models.CharField(max_length=50, null=True)),
                ('correctanswer', models.CharField(max_length=50, null=True)),
                ('elapsed_time', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cafa_it_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MappedItemAssessmentTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
                ('it', models.ForeignKey(to='assess.ItemTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='UserAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ci_id', models.IntegerField(null=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('at', models.ForeignKey(to='assess.AssessmentTemplate')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gradeduseritem',
            name='it',
            field=models.ForeignKey(to='assess.ItemTemplate'),
        ),
        migrations.AddField(
            model_name='gradeduseritem',
            name='ua',
            field=models.ForeignKey(to='assess.UserAssessment'),
        ),
    ]
