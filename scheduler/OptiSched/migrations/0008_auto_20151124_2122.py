# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0007_auto_20151124_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerequirementtime',
            name='day_of_week',
            field=models.CharField(max_length=1, choices=[(b'0', b'Monday'), (b'1', b'Tuesday'), (b'2', b'Wednesday'), (b'3', b'Thursday'), (b'4', b'Friday'), (b'5', b'Saturday'), (b'6', b'Sunday')]),
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementtime',
            unique_together=set([('day_of_week', 'erd_start_time', 'erd_requirement')]),
        ),
    ]
