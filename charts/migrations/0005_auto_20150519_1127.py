# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0004_testreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrun',
            name='report_id',
        ),
        migrations.AlterField(
            model_name='testrun',
            name='testplan',
            field=models.ForeignKey(verbose_name=b'the related Test Plan', to='charts.TestPlan'),
        ),
    ]
