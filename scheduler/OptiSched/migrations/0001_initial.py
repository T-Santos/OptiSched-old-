# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('date', models.DateField(default=datetime.date.today, serialize=False, primary_key=True)),
                ('day_start_time', models.TimeField(default=datetime.time(8, 0), verbose_name=b'Day Start Time')),
                ('day_end_time', models.TimeField(default=datetime.time(23, 59), verbose_name=b'Day End Time')),
            ],
        ),
        migrations.CreateModel(
            name='DateTimeRequest',
            fields=[
                ('request_date', models.DateField(serialize=False, primary_key=True)),
                ('request_start_time', models.TimeField(default=datetime.time(0, 0), verbose_name=b'Request Start Time')),
                ('request_end_time', models.TimeField(default=datetime.time(23, 59), verbose_name=b'Request End Time')),
                ('request_type', models.CharField(max_length=4, choices=[(b'VACA', b'Vacation'), (b'SICK', b'Sick'), (b'PREF', b'Preferred'), (b'SKIP', b'Cannot Work')])),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeRequirementDateTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erd_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('et_type', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTypeRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etd_employee_type_count', models.IntegerField()),
                ('etd_employee_type', models.ForeignKey(to='OptiSched.EmployeeType')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='PersonEmployeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pet_employee', models.ForeignKey(to='OptiSched.Person')),
                ('pet_employee_type', models.ForeignKey(to='OptiSched.EmployeeType')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField(verbose_name=b'Start Time')),
                ('end_time', models.TimeField(verbose_name=b'End Time')),
                ('employee', models.ForeignKey(to='OptiSched.Person')),
                ('shift_date', models.ForeignKey(to='OptiSched.Date')),
                ('shift_employee_type', models.ForeignKey(to='OptiSched.EmployeeType')),
            ],
        ),
        migrations.AddField(
            model_name='employeerequirementdatetime',
            name='erd_requirement',
            field=models.ForeignKey(to='OptiSched.EmployeeTypeRequirement'),
        ),
        migrations.AddField(
            model_name='datetimerequest',
            name='request_employee',
            field=models.ForeignKey(to='OptiSched.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='employeetyperequirement',
            unique_together=set([('etd_employee_type', 'etd_employee_type_count')]),
        ),
        migrations.AlterUniqueTogether(
            name='employeerequirementdatetime',
            unique_together=set([('erd_datetime', 'erd_requirement')]),
        ),
    ]
