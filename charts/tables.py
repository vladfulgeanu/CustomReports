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
from django.db.models import Q, Max
from django.conf.urls import url

class TestReportTable(ToasterTable):
    """Table of layers in Toaster"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self)
        self.default_orderby = "testrun_id"

    def setup_queryset(self, *args, **kwargs):
        testruns = TestRun.objects.filter(release=kwargs['release'])

        self.queryset = testruns.order_by(self.default_orderby)

    def setup_columns(self, *args, **kwargs):

        testrun_template = '''
        {% url 'charts:base_testrun' as base %}
        {% with base|add:data.testrun_id as link %}
        <a href="{{ link }}"> {{ data.testrun_id }} </a>
        {% endwith %}
        '''

        self.add_column(title="Test Run",
                        hideable=False,
                        orderable=True,
                        static_data_name="testrun_id",
                        static_data_template=testrun_template)


        self.add_column(title="Test Plan",
                        hideable=False,
                        orderable=True,
                        field_name="testplan__name")

        env_template = '''
        {% if data.target == data.hw %}
            <span>{{ data.target }}</span>
        {% else %}
            <span>{{ data.target }} on {{ data.hw }}</span>
        {% endif %}
        '''

        self.add_column(title="Environment",
                        hideable=False,
                        orderable=True,
                        static_data_name="target",
                        static_data_template=env_template)

        passed_template = '''
        {% with percentage=data.get_passed_percentage %}
        <span>{{ percentage }}%</span>
        {% endwith %}
        '''

        self.add_column(title="Passed",
                        hideable=False,
                        orderable=True,
                        static_data_name="testcaseresult_set",
                        static_data_template=passed_template)
 
        ## ....


# This needs to be staticaly defined here as django reads the url patterns
# on start up
urlpatterns = (
    url(r'testreport/(?P<release>[\w.]+)/(?P<cmd>\w+)*', TestReportTable.as_view(), name=TestReportTable.__name__.lower()),
)
