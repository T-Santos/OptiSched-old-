# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0003_auto_20151022_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeerequirementdatetime',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=22, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employeerequirementdatetime',
            name='erd_datetime',
            field=models.DateTimeField(),
        ),
    ]
