# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0003_auto_20150513_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('testreport_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('filters', models.CharField(max_length=10000)),
            ],
        ),
    ]
