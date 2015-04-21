# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_case_id', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=4, choices=[(b'PASS', b'pass'), (b'FAIL', b'fail')])),
                ('message', models.SlugField(max_length=15000)),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commit', models.CharField(max_length=100)),
                ('target', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('image_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='testresult',
            name='testrun',
            field=models.ForeignKey(to='charts.TestRun'),
        ),
    ]
