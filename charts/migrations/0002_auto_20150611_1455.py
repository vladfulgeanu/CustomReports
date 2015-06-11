# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
