from django.db import models
from django.forms import ModelForm

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