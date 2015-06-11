from django.db import models
from django.forms import ModelForm

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

	version = models.CharField(max_length=10, blank=True)
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

	def get_for_plan_env(self):
		return TestRun.objects.filter(release=self.release).filter(testplan=self.testplan, target=self.target, hw=self.hw)

	def get_total(self):
		total = 0
		for testrun in self.get_for_plan_env():
			total += testrun.testcaseresult_set.count()
		return total

	def get_run(self):
		run = 0
		for testrun in self.get_for_plan_env():
			run += testrun.testcaseresult_set.filter(~models.Q(result='idle')).count()
		return run

	def get_passed(self):
		passed = 0
		for testrun in self.get_for_plan_env():
			passed += testrun.testcaseresult_set.filter(result='pass').count()
		return passed

	def get_failed(self):
		failed = 0
		for testrun in self.get_for_plan_env():
			failed += testrun.testcaseresult_set.filter(result='fail').count()
		return failed

	def get_abs_passed_percentage(self):
		return ("%.2f" % ((self.get_passed() / float(self.get_total())) * 100)).rstrip('0').rstrip('.')

	def get_relative_passed_percentage(self):
		return ("%.2f" % ((self.get_passed() / float(self.get_run())) * 100)).rstrip('0').rstrip('.')

	def __str__(self):
		return self.testrun_id + " " + self.test_type + " " + self.release

class TestCaseResult(models.Model):
	RESULT_CHOICES = (
		('pass', 'pass'),
		('fail', 'fail'),
		('blocked', 'blocked'),
		('idle', 'idle')
	)

	testcase_id = models.CharField(max_length=10, primary_key=True)
	testrun = models.ForeignKey(TestRun)

	result = models.CharField(max_length=4, choices=RESULT_CHOICES)
	message = models.CharField(max_length=30000, blank=True)
	started_on = models.DateTimeField(blank = True)
	finished_on = models.DateTimeField(blank = True)
	attachments = models.CharField(max_length=1000, blank=True)
	comments = models.CharField(max_length=1000, blank=True)

	def __str__(self):
		return self.testcase.testcase_id + " " + self.result + "ed"

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
		fields = ['testrun_id', 'version', 'release', 'test_type', 'poky_commit', 'poky_branch', 'date', 'target', 'image_type', 'hw_arch', 
		'hw', 'host_os', 'other_layers_commits', 'ab_image_repo', 'services_running', 'package_versions_installed']

class TestCaseResultForm(ModelForm):
	class Meta:
		model = TestCaseResult
		fields = ['testcase_id', 'result', 'message', 'started_on', 'finished_on', 'attachments', 'comments']

class TestReportForm(ModelForm):
	class Meta:
		model = TestReport
		fields = ['filters']



