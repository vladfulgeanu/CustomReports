# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0002_auto_20150513_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcaseresult',
            name='attachments',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='testcaseresult',
            name='comments',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
