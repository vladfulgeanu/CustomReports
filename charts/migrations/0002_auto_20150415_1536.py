# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testrun',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='testresult',
            name='message',
            field=models.CharField(max_length=30000, blank=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='result',
            field=models.CharField(max_length=4, choices=[(b'pass', b'pass'), (b'fail', b'fail')]),
        ),
    ]
