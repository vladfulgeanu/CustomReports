from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.defaulttags import register
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django import forms
import json, collections, re

from .models import TestPlan, TestRun, TestCaseResult, TestReport
from . import tables

# Template filter to get the value given its coresponding key in a dictionary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# class ModelChoiceField(forms.ModelChoiceField):
# 	def label_from_instance(self, obj):
# 		return obj.release[:3]

class ReleaseForm(forms.Form):
	versions = forms.ModelChoiceField(queryset=TestRun.objects.all().order_by('-version').distinct('version'), to_field_name='version')


def search(request):

	query_string = ''
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

	return render(request, 'charts/search_results.html', {
			'query_string': query_string,
			'request' : request.GET.urlencode,
			'table_name' : tables.SearchTable.__name__.lower()
		})

def index(request, version=None):

	version_form = ReleaseForm()

	start = True

	if not version:
		latest_version = TestRun.objects.order_by('-version').distinct('version').values_list('version')[0][0]
	else:
		start = False
		latest_version = version

	testruns = {}

	uniq_release_testruns = TestRun.objects.filter(version=latest_version).distinct('release')

	for uniq_release_testrun in uniq_release_testruns:
		passed = failed = 0
		testruns_in_release = TestRun.objects.filter(release=uniq_release_testrun.release)
		for testrun_in_release in testruns_in_release:
			passed += testrun_in_release.testcaseresult_set.filter(result='passed').count()
			failed += testrun_in_release.testcaseresult_set.filter(result='failed').count()

		testruns[uniq_release_testrun.release.encode('ascii', 'ignore')] = {
			'release' : uniq_release_testrun.release,
			'passed' : passed,
			'failed' : failed
		}

	return render(request, 'charts/index.html', {
			'version_form' : version_form,
			'start' : start,
			'version' : latest_version,
			'testruns' : collections.OrderedDict(sorted(testruns.items(), reverse=True))
		})

def testrun_filter(request):

	results = None
	results_dict = collections.OrderedDict()
	draw_chart = False
	testplan_name = ''
	if request.GET:
		search_by = ('testplan', 'release', 'test_type', 'poky_commit', 'target', 'image_type', 'hw_arch', 'hw')
		query_attrs = dict([(param, val) for param, val in request.GET.iteritems() if param in search_by and val])
		results = TestRun.objects.filter(**query_attrs).order_by('start_date')

		draw_chart = True
		for testrun in results:
			results_dict[testrun.id] = {
				'date' : '%s' % testrun.start_date.strftime('%-d %b %H:%M %p'),
				'passed' : testrun.testcaseresult_set.filter(result='passed').count(),
				'failed' : testrun.testcaseresult_set.filter(result='failed').count()
			}

		if request.GET.get('testplan'):
			testplan_name = TestPlan.objects.get(id=request.GET.get('testplan')).name

	return render(request, 'charts/testrun_filter.html', {
			'release_form' : [release.encode("utf8") for release in TestRun.objects.distinct('release').values_list('release', flat=True)],
			'plan_form' : TestPlan.objects.distinct('name').all(),
			'type_form' : [ttype.encode("utf8") for ttype in TestRun.objects.distinct('test_type').values_list('test_type', flat=True)],
			'commit_form' : [commit.encode("utf8") for commit in TestRun.objects.distinct('poky_commit').values_list('poky_commit', flat=True)],
			'target_form' : [target.encode("utf8") for target in TestRun.objects.distinct('target').values_list('target', flat=True)],
			'itype_form' : [itype.encode("utf8") for itype in TestRun.objects.distinct('image_type').values_list('image_type', flat=True)],
			'hwa_form' : [hwa.encode("utf8") for hwa in TestRun.objects.distinct('hw_arch').values_list('hw_arch', flat=True)],
			'hw_form' : [hw.encode("utf8") for hw in TestRun.objects.distinct('hw').values_list('hw', flat=True)],
			'query' : request.GET.get('release', '') + " " + testplan_name + " " + request.GET.get('test_type', '') + " " +
					  request.GET.get('poky_commit', '') + " " + request.GET.get('target', '') + " " + request.GET.get('image_type', '') + " " +
					  request.GET.get('hw_arch', '') + " " + request.GET.get('hw', ''),
			'draw_chart' : draw_chart,
			'results_dict' : results_dict
		})


def testcase_filter(request):

	draw_chart = False
	is_empty = False
	if request.GET:
		if request.GET['name']:
			draw_chart = True
			if TestCaseResult.objects.filter(testcase_id=request.GET['name']).count() == 0:
				is_empty = True

	return render(request, 'charts/testcase_filter.html', {			'draw_chart' : draw_chart,
			'is_empty' : is_empty,
			'table_name' : tables.TestCaseTable.__name__.lower()
		})

def testrun(request, id):

	testrun = get_object_or_404(TestRun, pk = id)
	testcaseresults = testrun.testcaseresult_set.all()

	return render(request, 'charts/testrun.html', {
			'testrun'     : testrun,
			'passed'      : testcaseresults.filter(result='passed').count(),
			'failed'      : testcaseresults.filter(result='failed').count(),
			'blocked'     : testcaseresults.filter(result='blocked').count(),
			'idle'        : testcaseresults.filter(result='idle').count(),
			'testcaseresults' : testcaseresults
		})

def testreport(request, release):

	testreport = TestRun.objects.filter(release=release)


	passes = fails = 0
	for testrun in testreport:
		no_testcaseresults = testrun.testcaseresult_set.count()
		passes +=  no_testcaseresults - testrun.testcaseresult_set.filter(result='failed').count()
		fails +=  no_testcaseresults - testrun.testcaseresult_set.filter(result='passed').count()

	return render(request, 'charts/testreport.html', {
			'fails' : fails,
			'passes': passes,
			'release' : release,
			'testreport' : testreport,
			'table_name' : tables.TestReportTable.__name__.lower()
		})

def planenv(request, release, testplan, target, hw):

	failed = {}
	testruns = TestRun.objects.filter(release=release).filter(testplan_id=testplan, target=target, hw=hw)
	for testrun in testruns:
		failed[testrun.id] = testrun.testcaseresult_set.filter(result='failed').all()

	testplan_name = testruns[0].testplan.name

	return render(request, 'charts/planenv.html', {
			'testplan' : testplan_name,
			'target' : target,
			'hw' : hw,
			'testruns' : testruns,
			'failed' : failed
		})

"""
	testreports = []

	# TODO check for null
	lastest_testreports = get_list_or_404(TestReport)[-5:]
	
	for testreport in lastest_testreports:
		filters_dict = {}
		filters_json = json.loads(testreport.filters)
		for key, value in filters_json.iteritems():
			filters_dict[key] = value

		testreports.append(TestRun.objects.filter(**filters_dict))
"""