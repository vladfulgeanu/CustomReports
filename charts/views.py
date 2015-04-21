from django.shortcuts import get_list_or_404, render

from .models import TestRun, TestResult

def index(request):

	testrun_list = get_list_or_404(TestRun)

	return render(request, 'charts/index.html', {
			'testruns' : testrun_list
		})

def dashboard(request):

	testrun_list = get_list_or_404(TestRun)
	results = []

	for testrun in testrun_list:
		passed = testrun.testresult_set.filter(result="pass").count()
		results.append({
			'date'   : testrun.date,
		 	'passed' : passed,
			'failed' : testrun.testresult_set.count() - passed
		})

	return render(request, 'charts/dashboard.html', {
			'results' : results
		})