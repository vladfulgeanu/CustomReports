from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import TestRun, TestResult

def index(request):

	testruns = get_list_or_404(TestRun)

	return render(request, 'charts/index.html', {
			'testruns' : testruns
		})

def dashboard(request):

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
	testresults = testrun.testresult_set.all
	passed = testrun.testresult_set.filter(result="pass").count()

	return render(request, 'charts/testrun.html', {
			'date'        : testrun.date,
			'commit'      : testrun.commit,
			'target'      : testrun.target,
			'itype'       : testrun.image_type,
			'passed'      : passed,
			'failed'      : testrun.testresult_set.count() - passed,
			'testresults' : testresults
		})
