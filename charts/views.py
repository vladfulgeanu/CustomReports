from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse

from .models import TestRun, TestResult

def index(request):

	testrun_list = get_list_or_404(TestRun)

	return render(request, 'charts/index.html', {
			'testruns' : testrun_list
		})

def dashboard(request):

	testrun_list = get_list_or_404(TestRun)
	mydict = {}

	for testrun in testrun_list:
		passed = testrun.testresult_set.filter(result="pass").count()
		mydict[testrun.id] = {
			'date'   : testrun.date,
		 	'passed' : passed,
			'failed' : testrun.testresult_set.count() - passed
		}

	return render(request, 'charts/dashboard.html', {
			'dict' : mydict
		})