# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCaseResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcase_id', models.CharField(max_length=40)),
                ('result', models.CharField(choices=[(b'passed', b'passed'), (b'failed', b'failed'), (b'blocked', b'blocked'), (b'idle', b'idle')], max_length=7)),
                ('message', models.CharField(blank=True, max_length=30000)),
                ('started_on', models.DateTimeField(blank=True, null=True)),
                ('finished_on', models.DateTimeField(blank=True, null=True)),
                ('attachments', models.CharField(blank=True, max_length=1000)),
                ('comments', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('product', models.CharField(max_length=30)),
                ('product_version', models.CharField(max_length=10)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=100)),
                ('version', models.CharField(blank=True, max_length=10)),
                ('plan_type', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('testreport_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('filters', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(blank=True, max_length=10)),
                ('release', models.CharField(blank=True, max_length=30)),
                ('test_type', models.CharField(choices=[(b'Weekly', b'Weekly'), (b'Full Pass', b'Full Pass')], max_length=15)),
                ('poky_commit', models.CharField(max_length=100)),
                ('poky_branch', models.CharField(max_length=15)),
                ('start_date', models.DateTimeField()),
                ('stop_date', models.DateTimeField(blank=True, null=True)),
                ('target', models.CharField(blank=True, max_length=30)),
                ('image_type', models.CharField(blank=True, max_length=30)),
                ('hw_arch', models.CharField(blank=True, max_length=15)),
                ('hw', models.CharField(blank=True, max_length=30)),
                ('host_os', models.CharField(blank=True, max_length=30)),
                ('other_layers_commits', models.CharField(blank=True, max_length=500)),
                ('ab_image_repo', models.CharField(blank=True, max_length=100)),
                ('services_running', models.CharField(blank=True, max_length=10000)),
                ('package_versions_installed', models.CharField(blank=True, max_length=20000)),
                ('testplan', models.ForeignKey(to='charts.TestPlan', verbose_name=b'the related Test Plan')),
            ],
        ),
        migrations.AddField(
            model_name='testcaseresult',
            name='testrun',
            field=models.ForeignKey(to='charts.TestRun'),
        ),
    ]
