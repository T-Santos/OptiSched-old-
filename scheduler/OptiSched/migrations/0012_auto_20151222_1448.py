# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0011_auto_20151204_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='day_start_time',
            field=models.TimeField(default=datetime.time(8, 0), verbose_name=b'Day Start Time'),
        ),
    ]
