# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetype',
            name='id',
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='et_type',
            field=models.CharField(max_length=60, serialize=False, primary_key=True),
        ),
    ]
