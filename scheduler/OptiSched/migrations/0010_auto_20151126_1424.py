# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OptiSched', '0009_auto_20151124_2143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeerequirementtime',
            old_name='erd_requirement',
            new_name='ert_requirement',
        ),
        migrations.RenameField(
            model_name='employeerequirementtime',
            old_name='erd_start_time',
            new_name='ert_start_time',
        ),
        migrations.RenameField(
            model_name='employeetyperequirement',
            old_name='etd_employee_type',
            new_name='etr_employee_type',
        ),
        migrations.RenameField(
            model_name='employeetyperequirement',
            old_name='etd_employee_type_count',
            new_name='etr_employee_type_count',
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementtime',
            unique_together=set([('day_of_week', 'ert_start_time', 'ert_requirement')]),
        ),
        migrations.AlterUniqueTogether(
            name='employeetyperequirement',
            unique_together=set([('etr_employee_type', 'etr_employee_type_count')]),
        ),
    ]
