from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    url(r'^$', 'charts.views.index', name='index'),
    url(r'^dashboard$', 'charts.views.dashboard', name='dashboard'),
    url(r'^testrun/(?P<id>[0-9]+)$', 'charts.views.testrun', name='testrun'),
    url(r'^testrun/', lambda x: HttpResponseBadRequest(), name='base_testrun'),
    url(r'^testcase/(?P<id>[0-9]+)$', 'charts.views.testcase', name='testcase'),
    url(r'^testcase/', lambda x: HttpResponseBadRequest(), name='base_testcase'),
)