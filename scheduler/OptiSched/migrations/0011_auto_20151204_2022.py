# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0010_auto_20151126_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='person_max_hours_per_shift',
            field=models.IntegerField(default=8),
        ),
        migrations.AddField(
            model_name='person',
            name='person_max_hours_per_week',
            field=models.IntegerField(default=40),
        ),
        migrations.AddField(
            model_name='person',
            name='person_min_hours_per_shift',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='person',
            name='person_min_hours_per_week',
            field=models.IntegerField(default=25),
        ),
        migrations.AlterField(
            model_name='date',
            name='day_start_time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name=b'Day Start Time'),
        ),
    ]
