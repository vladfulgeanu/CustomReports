from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import register
from django import forms
import collections

from .models import TestPlan, TestRun, TestCaseResult
from . import tables

# Template filter to get the value given its coresponding key in a dictionary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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

def index(request, latest_version=None):

    version_form = ReleaseForm()

    start = True

    if not latest_version:
        version = TestRun.objects.order_by('-version').distinct('version').values_list('version')[0][0]
    else:
        start = False
        version = latest_version

    testruns = {}

    all_releases = TestRun.objects.filter(version=version).distinct('release').values_list('release', flat=True)

    for release in all_releases:
        passed = failed = 0
        testruns_in_release = TestRun.objects.filter(release=release)
        for testrun_in_release in testruns_in_release:
            passed += testrun_in_release.testcaseresult_set.filter(result='passed').count()
            failed += testrun_in_release.testcaseresult_set.filter(result='failed').count()

        testruns[release.encode('ascii', 'ignore')] = {
            'passed' : passed,
            'failed' : failed
        }

    return render(request, 'charts/index.html', {
        'version_form' : version_form,
        'start' : start,
        'version' : version,
        'testruns' : collections.OrderedDict(sorted(testruns.items(), reverse=True))
        })

# returns a list used for creating a form with all distinct entries of given field name from Test Runs
def get_field_form(fieldname):

	return [entry.encode("utf8") for entry in TestRun.objects.distinct(fieldname).values_list(fieldname, flat=True)]

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
        'release_form' : get_field_form('release'),
        'plan_form' : TestPlan.objects.distinct('name').all(),
        'type_form' : get_field_form('test_type'),
        'commit_form' : get_field_form('poky_commit'),
        'target_form' : get_field_form('target'),
        'itype_form' : get_field_form('image_type'),
        'hwa_form' : get_field_form('hw_arch'),
        'hw_form' : get_field_form('hw'),
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

    return render(request, 'charts/testcase_filter.html', {
        'draw_chart' : draw_chart,
        'is_empty' : is_empty,
        'table_name' : tables.TestCaseTable.__name__.lower()
        })

def testrun(request, id):

    testrun = get_object_or_404(TestRun, pk=id)
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
        passes += testrun.testcaseresult_set.filter(result='passed').count()
        fails += testrun.testcaseresult_set.filter(result='failed').count()

    return render(request, 'charts/testreport.html', {
        'fails' : fails,
        'passes': passes,
        'release' : release,
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
