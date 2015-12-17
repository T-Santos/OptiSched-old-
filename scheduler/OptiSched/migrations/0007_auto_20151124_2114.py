# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0006_auto_20151124_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRequirementTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_week', models.CharField(max_length=1, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
                ('erd_start_time', models.TimeField(default=datetime.time(0, 0), verbose_name=b'Effective Hour')),
                ('erd_requirement', models.ForeignKey(to='OptiSched.EmployeeTypeRequirement')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementdatetime',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='employeerequirementdatetime',
            name='erd_requirement',
        ),
        migrations.DeleteModel(
            name='EmployeeRequirementDateTime',
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementtime',
            unique_together=set([('day_of_week', 'erd_start_time')]),
        ),
    ]
