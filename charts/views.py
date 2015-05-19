from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.db.models import Q
import json

from .models import TestPlan, TestRun, TestCase, TestCaseResult, TestReport

def index(request):

	testreports = []

	# TODO check for null
	lastest_testreports = get_list_or_404(TestReport)[-5:]
	
	for testreport in lastest_testreports:
		filters_dict = {}
		filters_json = json.loads(testreport.filters)
		for key, value in filters_json.iteritems():
			filters_dict[key] = value

		testreports.append(TestRun.objects.filter(**filters_dict))

	return render(request, 'charts/index.html', {
			'latest' : testreports[0],
			'other'  : testreports[1:]
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
		passed = testrun.testresult_set.filter(result="pass").count()
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
	passed = testrun.testcaseresult_set.filter(result="pass").count()

	return render(request, 'charts/testrun.html', {
			'date'        : testrun.date,
			'commit'      : testrun.poky_commit,
			'target'      : testrun.target,
			'itype'       : testrun.image_type,
			'passed'      : passed,
			'failed'      : testrun.testcaseresult_set.count() - passed,
			'testresults' : testcaseresults
		})
