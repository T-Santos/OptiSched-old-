# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0002_auto_20151022_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeerequirementdatetime',
            name='id',
        ),
        migrations.AlterField(
            model_name='employeerequirementdatetime',
            name='erd_datetime',
            field=models.DateTimeField(serialize=False, primary_key=True),
        ),
    ]
