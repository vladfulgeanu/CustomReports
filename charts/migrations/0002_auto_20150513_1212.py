# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='test_type',
            field=models.CharField(max_length=15, choices=[(b'Weekly', b'Weekly'), (b'Full Pass', b'Full Pass')]),
        ),
    ]
