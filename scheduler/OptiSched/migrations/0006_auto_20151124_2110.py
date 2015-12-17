# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0005_auto_20151101_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRequirementDateTimeOverride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erd_datetime', models.DateTimeField()),
                ('erd_requirement', models.ForeignKey(to='OptiSched.EmployeeTypeRequirement')),
            ],
        ),
        migrations.AddField(
            model_name='employeerequirementdatetime',
            name='day_of_week',
            field=models.CharField(default=0, max_length=1, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeerequirementdatetime',
            name='erd_start_time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name=b'Effective Hour'),
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementdatetime',
            unique_together=set([('day_of_week', 'erd_start_time')]),
        ),
        migrations.RemoveField(
            model_name='employeerequirementdatetime',
            name='erd_datetime',
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementdatetimeoverride',
            unique_together=set([('erd_datetime', 'erd_requirement')]),
        ),
    ]
