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

from charts.widgets import ToasterTable
from charts.models import TestRun, TestCaseResult
from django.db.models import Q
from django.db.models import Count, Max, Min, Sum, Avg
from django.conf.urls import url
import re, urlparse

class TestReportTable(ToasterTable):
    """Table of layers in Toaster"""
    """Table used inside a particular release's page"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self, True)
        self.default_orderby = "target"

    def setup_queryset(self, *args, **kwargs):
        testruns = TestRun.objects.filter(release=kwargs['release']).distinct('testplan', 'target', 'hw')

        self.queryset = testruns.order_by(self.default_orderby)

    def setup_columns(self, *args, **kwargs):

        testrun_template = '''\
        {% for testrun in data.get_for_plan_env %}\
            <a href="{% url 'charts:testrun' testrun.id %}">{{ testrun.id }} </a>\
        {% endfor %}\
        '''

        self.add_column(title="Test Run",
                        hideable=False,
                        orderable=False,
                        static_data_name="testrun_id",
                        static_data_template=testrun_template)

        planenv_template = '''\
        {% url 'charts:plan_env' data.release data.testplan.id data.target data.hw as link %}\
        {% if data.target == data.hw %}\
            <a href="{{ link }}">{{ data.testplan.name }} on {{ data.hw }} </a>\
        {% else %}\
            <a href="{{ link }}">{{ data.testplan.name }} with {{ data.target }} on {{ data.hw }} </a>\
        {% endif %}\
        '''

        self.add_column(
            title="Test Plan per environment",
            hideable=False,
            orderable=False,
            static_data_name="plan_env",
            static_data_template=planenv_template)

        total_template = '''{% with total=data.get_total %}<span id="total">{{ total }}</span>{% endwith %}'''

        self.add_column(
            title="Total",
            hideable=False,
            orderable=False,
            static_data_name="total",
            static_data_template=total_template)


        run_template = '''{% with run=data.get_run %}<span id="run">{{ run }}</span>{% endwith %}'''

        self.add_column(
            title="Run",
            hideable=False,
            orderable=False,
            static_data_name="run",
            static_data_template=run_template)

        passed_template = '''{% with passed=data.get_passed %}<span id="passed">{{ passed }}</span>{% endwith %}'''

        self.add_column(
            title="Passed",
            hideable=False,
            orderable=False,
            static_data_name="passed",
            static_data_template=passed_template)


        failed_template = '''{% with failed=data.get_failed %}{% if failed == 0 %}<span id="failed" class="text-success">{{ failed }}</span>{% else %}<span id="failed" class="text-danger">{{ failed }}</span>{% endif %}{% endwith %}'''

        self.add_column(
            title="Failed",
            hideable=False,
            orderable=False,
            static_data_name="failed",
            static_data_template=failed_template)

        # total = self.queryset.annotate(total=Count('testcaseresult'))
        # total_passed = self.queryset.annotate(passed=Sum(testcaseresult__result__in=['pass']))
        # print total + "   " + total_passed
        abs_pass_template = '''\
        {% with percentage=data.get_abs_passed_percentage %}\
        <span class=\
        {% if percentage >= "90" %}\
            "text-success"\
        {% elif percentage >= "80" %}\
            "text-warning"\
        {% else %}\
            "text-danger"\
        {% endif %}\
        >{{ percentage }}%</span>\
        {% endwith %}\
        '''

        self.add_column(
            title="Pass/Total",
            hideable=False,
            orderable=False,
            static_data_name="pass_total",
            static_data_template=abs_pass_template)

        relative_pass_template = '''\
        {% with percentage=data.get_relative_passed_percentage %}\
        <span class=\
        {% if percentage >= "90" %}\
            "text-success"\
        {% elif percentage >= "80" %}\
            "text-warning"\
        {% else %}\
            "text-danger"\
        {% endif %}\
        >{{ percentage }}%</span>\
        {% endwith %}\
        '''

        self.add_column(
            title="Pass/Run",
            hideable=False,
            orderable=False,
            static_data_name="pass_run",
            static_data_template=relative_pass_template)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """ Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    """ Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    """
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class SearchTable(ToasterTable):
    """Table of layers in Toaster"""
    """Table used inside search results page"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self, False)
        self.default_orderby = "id"

    def setup_queryset(self, *args, **kwargs):

        query_string = ''
        found_entries = None

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query = urlparse.urlparse(self.request.get_full_path()).query
            query_string = urlparse.parse_qs(query)['q'][0].encode('ascii', 'ignore').replace('+', ' ').replace('%22', '"')

        entry_query = get_query(
            query_string,
            ['testplan__name', 'version', 'release', 'test_type', 'poky_commit',
             'poky_branch', 'target', 'image_type', 'hw_arch', 'hw'])

        found_entries = TestRun.objects.filter(entry_query)

        self.queryset = found_entries.order_by(self.default_orderby)

        if self.queryset.count() == 0:
            self.title = "No results found"

    def setup_columns(self, *args, **kwargs):

        testrun_template = '''<a href="{% url 'charts:testrun' data.id %}">{{ data.id }} </a>'''

        self.add_column(title="Test Run",
                        hideable=False,
                        orderable=True,
                        static_data_name="id",
                        static_data_template=testrun_template)

        self.add_column(title="Test Plan",
                        hideable=False,
                        orderable=True,
                        field_name="testplan__name")

        self.add_column(title="Release",
                        hideable=False,
                        orderable=True,
                        field_name='release')

        self.add_column(title="Test Type",
                        hideable=False,
                        orderable=True,
                        field_name='test_type')

        self.add_column(title="Target",
                        hideable=False,
                        orderable=True,
                        field_name='target')


        self.add_column(title="Image type",
                        hideable=False,
                        orderable=True,
                        field_name='image_type')

        self.add_column(title="HW arch",
                        hideable=False,
                        orderable=True,
                        field_name='hw_arch')

        self.add_column(title="HW",
                        hideable=False,
                        orderable=True,
                        field_name='hw')

class TestCaseTable(ToasterTable):
    """Table of layers in Toaster"""
    """Table used inside a TestCase filter page page"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self, False)

    def setup_queryset(self, *args, **kwargs):

        results = None

        if self.request.GET:
            if self.request.GET['name']:
                query = urlparse.urlparse(self.request.get_full_path()).query
                query_string = urlparse.parse_qs(query)['name'][0].encode('ascii', 'ignore')
                results = TestCaseResult.objects.filter(testcase_id=query_string).order_by('-testrun__start_date')

        self.queryset = results

        if self.queryset.count() == 0:
            self.title = "No results found"

    def setup_columns(self, *args, **kwargs):

        date_template = '''<a href="{% url 'charts:testrun' data.testrun.id %}"> {{ data.testrun.start_date|date:"d M Y P" }} </a>'''

        self.add_column(title="Date",
                        hideable=False,
                        orderable=True,
                        static_data_name="testrun__start_date",
                        static_data_template=date_template)

        result_template = '''\
        <span class=\
        {% if data.result == 'passed' %}\
        "text-success"\
        {% else %}\
        "text-danger"\
        {% endif %}>\
        {{ data.result }} </span>'''

        self.add_column(title="Status",
                        hideable=False,
                        orderable=True,
                        static_data_name="result",
                        static_data_template=result_template)

        self.add_column(title="Commit",
                        hideable=False,
                        orderable=True,
                        field_name="testrun__poky_commit")

        self.add_column(title="Release",
                        hideable=False,
                        orderable=True,
                        field_name="testrun__release")


# This needs to be staticaly defined here as django reads the url patterns
# on start up
urlpatterns = (
    url(r'testreport/(?P<release>[\w.]+)/(?P<cmd>\w+)*', TestReportTable.as_view(), name=TestReportTable.__name__.lower()),
    url(r'search/(?P<cmd>\w+)*', SearchTable.as_view(), name=SearchTable.__name__.lower()),
    url(r'testcasefilter/(?P<cmd>\w+)*', TestCaseTable.as_view(), name=TestCaseTable.__name__.lower())
)
