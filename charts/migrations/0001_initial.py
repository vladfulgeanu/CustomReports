# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('testcase_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('summary', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=100)),
                ('tester', models.CharField(max_length=100, blank=True)),
                ('category', models.CharField(max_length=15)),
                ('priority', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='TestCaseResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(max_length=4, choices=[(b'pass', b'pass'), (b'fail', b'fail')])),
                ('message', models.CharField(max_length=30000, blank=True)),
                ('started_on', models.DateTimeField(blank=True)),
                ('finished_on', models.DateTimeField(blank=True)),
                ('attachments', models.CharField(max_length=1000, blank=True)),
                ('comments', models.CharField(max_length=1000, blank=True)),
                ('testcase', models.ForeignKey(to='charts.TestCase')),
            ],
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('product', models.CharField(max_length=30)),
                ('product_version', models.CharField(max_length=10)),
                ('created', models.DateTimeField()),
                ('author', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=10, blank=True)),
                ('plan_type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('testreport_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('filters', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('testrun_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('y_version', models.CharField(max_length=10, blank=True)),
                ('release', models.CharField(max_length=30, blank=True)),
                ('test_type', models.CharField(max_length=15, choices=[(b'Weekly', b'Weekly'), (b'Full Pass', b'Full Pass')])),
                ('poky_commit', models.CharField(max_length=100)),
                ('poky_branch', models.CharField(max_length=15)),
                ('date', models.DateTimeField()),
                ('target', models.CharField(max_length=30, blank=True)),
                ('image_type', models.CharField(max_length=30, blank=True)),
                ('hw_arch', models.CharField(max_length=15, blank=True)),
                ('hw', models.CharField(max_length=30, blank=True)),
                ('host_os', models.CharField(max_length=30, blank=True)),
                ('other_layers_commits', models.CharField(max_length=500, blank=True)),
                ('ab_image_repo', models.CharField(max_length=100, blank=True)),
                ('services_running', models.CharField(max_length=10000, blank=True)),
                ('package_versions_installed', models.CharField(max_length=20000, blank=True)),
                ('testplan', models.ForeignKey(verbose_name=b'the related Test Plan', to='charts.TestPlan')),
            ],
        ),
        migrations.AddField(
            model_name='testcaseresult',
            name='testrun',
            field=models.ForeignKey(to='charts.TestRun'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='testplan',
            field=models.ForeignKey(to='charts.TestPlan'),
        ),
    ]
