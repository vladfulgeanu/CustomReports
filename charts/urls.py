from django.http import HttpResponseBadRequest
from django.conf.urls import patterns, url, include

from . import views, tables

urlpatterns = patterns('',

    url(r'^$', 'charts.views.index', name='index'),
    url(r'^(?P<version>[0-9.]+)$', 'charts.views.index', name='index_2'),
    url(r'^dashboard$', 'charts.views.dashboard', name='dashboard'),
    url(r'^testrun/(?P<id>[0-9]+)$', 'charts.views.testrun', name='testrun'),
    url(r'^testrun/', lambda x: HttpResponseBadRequest(), name='base_testrun'),
    url(r'^testcase/(?P<id>[0-9]+)$', 'charts.views.testcase', name='testcase'),
    url(r'^testcase/', lambda x: HttpResponseBadRequest(), name='base_testcase'),
    url(r'^testreport/(?P<release>[\w.]+)$', 'charts.views.testreport', name='testreport'),
    url(r'^testreport/(?P<release>[\w.]+)/(?P<testplan>[0-9]+)/(?P<target>[\w.]+)/(?P<hw>[\w.-]+)$', 'charts.views.planenv', name='plan_env'),
    url(r'^testreport/', lambda x: HttpResponseBadRequest(), name='base_testreport'),
    url(r'^xhr_tables/', include('charts.tables')),

)