from django.db import models
from django.forms import ModelForm
"""
class TestRun(models.Model):
	commit = models.CharField(max_length=100)
	target = models.CharField(max_length=100)
	date = models.DateField()
	image_type = models.CharField(max_length=100)

	class Meta:
		ordering = ['date']

	def __str__(self):
		return "commit: " + self.commit + ", on: " + self.target + ", date: " + self.date

class TestResult(models.Model):
	RESULT_CHOICES = (
		('pass', 'pass'),
		('fail', 'fail')
	)

	testrun = models.ForeignKey(TestRun)
	test_case_id = models.CharField(max_length=200)
	result = models.CharField(max_length=4, choices=RESULT_CHOICES)
	message = models.CharField(max_length=30000, blank=True)

	def __str__(self):
		return self.test_case_id + " result is: " + self.result

class TestRunForm(ModelForm):
	class Meta:
		model = TestRun
		fields = ['commit', 'target', 'date', 'image_type']

class TestResultForm(ModelForm):
	class Meta:
		model = TestResult
		fields = ['test_case_id', 'result', 'message']
"""

class TestPlan(models.Model):
	name = models.CharField(max_length=30)
	product = models.CharField(max_length=30)
	product_version = models.CharField(max_length=10)
	created = models.DateTimeField()
	author = models.CharField(max_length=100)
	version = models.CharField(max_length=10, blank=True)
	plan_type = models.CharField(max_length=30)

	def __str__(self):
		return self.name + " version: " + self.product_version

class TestRun(models.Model):
	TYPE_CHOICES = (
		('Weekly', 'Weekly'),
		('Full Pass', 'Full Pass')
	)
	testrun_id = models.CharField(max_length=10, primary_key=True)
	testplan = models.ForeignKey(TestPlan, verbose_name="the related Test Plan")

	release = models.CharField(max_length=30, blank=True)
	test_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
	poky_commit = models.CharField(max_length=100)
	poky_branch = models.CharField(max_length=15)
	date = models.DateTimeField()

	target = models.CharField(max_length=30, blank=True)
	image_type = models.CharField(max_length=30, blank=True)
	hw_arch = models.CharField(max_length=15, blank=True)
	hw = models.CharField(max_length=30, blank=True)
	host_os = models.CharField(max_length=30, blank=True)
	other_layers_commits = models.CharField(max_length=500, blank=True)
	ab_image_repo = models.CharField(max_length=100, blank=True)
	services_running = models.CharField(max_length=10000, blank=True)
	package_versions_installed = models.CharField(max_length=20000, blank=True)

	def __str__(self):
		return self.testrun_id + " " + self.test_type + " " + self.release

class TestCase(models.Model):
	testcase_id = models.CharField(max_length=10, primary_key=True)
	testplan = models.ForeignKey(TestPlan)

	summary = models.CharField(max_length=500)
	author = models.CharField(max_length=100)
	tester = models.CharField(max_length=100, blank=True)
	category = models.CharField(max_length=15)
	priority = models.CharField(max_length=15)

	def __str__(self):
		return self.testcase_id

class TestCaseResult(models.Model):
	RESULT_CHOICES = (
		('pass', 'pass'),
		('fail', 'fail')
	)

	testcase = models.ForeignKey(TestCase)
	testrun = models.ForeignKey(TestRun)

	result = models.CharField(max_length=4, choices=RESULT_CHOICES)
	message = models.CharField(max_length=30000, blank=True)
	started_on = models.DateTimeField(blank = True)
	finished_on = models.DateTimeField(blank = True)
	attachments = models.CharField(max_length=1000, blank=True)
	comments = models.CharField(max_length=1000, blank=True)

	def __str__(self):
		return self.testrun.testcase_id + " " + self.result + "ed"

class TestReport(models.Model):
	testreport_id = models.CharField(max_length=10, primary_key=True)
	filters = models.CharField(max_length=10000)

	def __str__(self):
		return self.testreport_id


class TestPlanForm(ModelForm):
	class Meta:
		model = TestPlan
		fields = ['name', 'product', 'product_version', 'created', 'author', 'version', 'plan_type']

class TestRunForm(ModelForm):
	class Meta:
		model = TestRun
		fields = ['testrun_id', 'release', 'test_type', 'poky_commit', 'poky_branch', 'date', 'target', 'image_type', 'hw_arch', 
		'hw', 'host_os', 'other_layers_commits', 'ab_image_repo', 'services_running', 'package_versions_installed']

class TestCaseForm(ModelForm):
	class Meta:
		model = TestCase
		fields = ['testcase_id', 'summary', 'author', 'tester', 'category', 'priority']


class TestCaseResultForm(ModelForm):
	class Meta:
		model = TestCaseResult
		fields = ['result', 'message', 'started_on', 'finished_on', 'attachments', 'comments']

class TestReportForm(ModelForm):
	class Meta:
		model = TestReport
		fields = ['filters']



