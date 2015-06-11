from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.defaulttags import register
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django import forms
import json, collections

from .models import TestPlan, TestRun, TestCaseResult, TestReport
from . import tables

# Template filter to get the value given its coresponding key in a dictionary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class ModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.release[:3]

class ReleaseForm(forms.Form):
	versions = ModelChoiceField(queryset=TestRun.objects.all().order_by('-version').distinct('version'), to_field_name="version")

def index(request, version=None):

	version_form = ReleaseForm()
	# if request.method == 'POST':
	# 	version_form = ReleaseForm(request.POST)
	# 	if version_form.is_valid:
	# 		return HttpResponseRedirect(reverse('charts:dashboard'))

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
			passed += testrun_in_release.testcaseresult_set.filter(result='pass').count()
			failed += testrun_in_release.testcaseresult_set.filter(result='fail').count()

		testruns[uniq_release_testrun.release.encode('ascii', 'ignore')] = {
			'rc' : uniq_release_testrun.release[-3:],
			'passed' : passed,
			'failed' : failed
		}

	return render(request, 'charts/index.html', {
			'version_form' : version_form,
			'start' : start,
			'version' : latest_version,
			'testruns' : collections.OrderedDict(sorted(testruns.items(), reverse=True))
		})
	

def dashboard(request):
	
	# latest date for testruns with report_id not null
	latest_date = TestRun.objects.exclude(result_id__isnull=False).latest('date').date

	# get report_id with latest_date
	latest_report = TestRun.objects.filter(date=latest_date)[0].report_id

	# get latest report testruns
	latest_testruns = TestRun.objects.filter(report_id=latest_report)

	all_testruns = get_list_or_404(TestRun)
	testruns = []

	last_testruns = all_testruns[-10:]
	for testrun in last_testruns:
		passed = testrun.testresult_set.filter(result='pass').count()
		testruns.append({
			'id'     : testrun.id,
			'date'   : testrun.date,
			'commit' : testrun.commit,
			'target' : testrun.target,
			'itype'  : testrun.image_type,
		 	'passed' : passed,
			'failed' : testrun.testresult_set.count() - passed
		})

	return render(request, 'charts/dashboard.html', {
			'testruns' : testruns
		})

def testrun(request, id):

	testrun = get_object_or_404(TestRun, pk = id)
	testcaseresults = testrun.testcaseresult_set.all
	passed = testrun.testcaseresult_set.filter(result='pass').count()

	return render(request, 'charts/testrun.html', {
			'date'        : testrun.date,
			'commit'      : testrun.poky_commit,
			'target'      : testrun.target,
			'itype'       : testrun.image_type,
			'passed'      : passed,
			'failed'      : testrun.testcaseresult_set.count() - passed,
			'testcaseresults' : testcaseresults
		})

def testreport(request, release):

	testreport = TestRun.objects.filter(release=release)


	passes = fails = 0
	for testrun in testreport:
		no_testcaseresults = testrun.testcaseresult_set.count()
		passes +=  no_testcaseresults - testrun.testcaseresult_set.filter(result='fail').count()
		fails +=  no_testcaseresults - testrun.testcaseresult_set.filter(result='pass').count()

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
		failed[testrun.testrun_id] = testrun.testcaseresult_set.filter(result='fail').all()

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