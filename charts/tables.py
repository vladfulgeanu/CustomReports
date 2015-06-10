#
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Toaster Implementation
#
# Copyright (C) 2015        Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from widgets import ToasterTable
from charts.models import TestRun
from django.db.models import Q
from django.db.models import Count, Max, Min, Sum, Avg
from django.conf.urls import url

class TestReportTable(ToasterTable):
    """Table of layers in Toaster"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self, True)
        self.default_orderby = "target"

    def setup_queryset(self, *args, **kwargs):
        testruns = TestRun.objects.filter(release=kwargs['release']).distinct('testplan', 'target', 'hw')

        self.queryset = testruns.order_by(self.default_orderby)

    def setup_columns(self, *args, **kwargs):

        testrun_template = '''\
        {% url 'charts:base_testrun' as base %}\
        {% for testrun in data.get_for_plan_env %}\
            {% with base|add:testrun.testrun_id as link %}\
            <a href="{{ link }}">{{ testrun.testrun_id }} </a>\
            {% endwith %}\
        {% endfor %}\
        '''

        self.add_column(title="Test Run",
                        hideable=False,
                        orderable=False,
                        static_data_name="testrun_id",
                        static_data_template=testrun_template)

        custom_template = '''\
        {% url 'charts:plan_env' data.release data.testplan.id data.target data.hw as link %}\
        {% if data.target == data.hw %}\
            <a href="{{ link }}">{{ data.testplan.name }} on {{ data.hw }} </a>\
        {% else %}\
            <a href="{{ link }}">{{ data.testplan.name }} with {{ data.target }} on {{ data.hw }} </a>\
        {% endif %}\
        '''

        self.add_column(title="Test Plan per environment",
                hideable=False,
                orderable=False,
                static_data_name="plan_env",
                static_data_template=custom_template)

        total_template = "{% with total=data.get_total %}<span id='total'>{{ total }}</span>{% endwith %}"

        self.add_column(title="Total",
                hideable=False,
                orderable=False,
                static_data_name="total",
                static_data_template=total_template)


        run_template = "{% with run=data.get_run %}<span id='run'>{{ run }}</span>{% endwith %}"

        self.add_column(title="Run",
                hideable=False,
                orderable=False,
                static_data_name="run",
                static_data_template=run_template)

        passed_template = "{% with passed=data.get_passed %}<span id='passed'>{{ passed }}</span>{% endwith %}"

        self.add_column(title="Passed",
                hideable=False,
                orderable=False,
                static_data_name="passed",
                static_data_template=passed_template)


        failed_template = '''{% with failed=data.get_failed %}{% if failed == 0 %}<span id='failed' class=\"text-success\">{{ failed }}</span>{% else %}<span id='failed' class=\"text-danger\">{{ failed }}</span>{% endif %}{% endwith %}'''

        self.add_column(title="Failed",
                hideable=False,
                orderable=False,
                static_data_name="failed",
                static_data_template=failed_template)

        # total = self.queryset.annotate(total=Count('testcaseresult'))
        # total_passed = self.queryset.annotate(passed=Sum(testcaseresult__result__in=['pass']))
        # print total + "   " + total_passed
        abs_pass_template = '''\
        {% with percentage=data.get_abs_passed_percentage %}\
        <span>{{ percentage }}%</span>\
        {% endwith %}\
        '''

        self.add_column(title="Pass/Total",
                        hideable=False,
                        orderable=False,
                        static_data_name="pass_total",
                        static_data_template=abs_pass_template)

        relative_pass_template = '''\
        {% with percentage=data.get_relative_passed_percentage %}\
        <span>{{ percentage }}%</span>\
        {% endwith %}\
        '''

        self.add_column(title="Pass/Run",
                        hideable=False,
                        orderable=False,
                        static_data_name="pass_run",
                        static_data_template=relative_pass_template)
 
        ## ....


# This needs to be staticaly defined here as django reads the url patterns
# on start up
urlpatterns = (
    url(r'testreport/(?P<release>[\w.]+)/(?P<cmd>\w+)*', TestReportTable.as_view(), name=TestReportTable.__name__.lower()),
)
