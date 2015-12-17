# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0008_auto_20151124_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerequirementtime',
            name='day_of_week',
            field=models.IntegerField(choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
        ),
    ]
