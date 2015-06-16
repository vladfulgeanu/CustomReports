#! /usr/bin/env python

import json
import os, sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), "customreports/"))
os.environ["DJANGO_SETTINGS_MODULE"] = "customreports.settings"

django.setup()

from charts.models import TestPlan, TestRunForm, TestCaseResultForm
from django.shortcuts import get_object_or_404

try:
	log_file = str(sys.argv[1])
	version = str(sys.argv[2])
	release = str(sys.argv[3])
	test_type = str(sys.argv[4])
	poky_commit = str(sys.argv[5])
	poky_branch = str(sys.argv[6])
	start_date = str(sys.argv[7])
	target = str(sys.argv[8])
	image_type = str(sys.argv[9])
	hw_arch = str(sys.argv[10])
	hw = str(sys.argv[11])

except IndexError, NameError:
	print "Usage: add_testrun <log_file> \"<version>\" \"<release>\" \"<test_type>\" \"<poky_commit>\" \"<poky_branch>\" \"<start_date>\" \"<target>\" \"<image_type>\" \"<hw_arch>\" \"<hw>\""
	sys.exit(1)


testrun = {
	'version' : version,
	'release' : release,
	'test_type' : test_type,
	'poky_commit' : poky_commit,
	'poky_branch' : poky_branch,
	'start_date' : start_date,
	'target' : target,
	'image_type' : image_type,
	'hw_arch' : hw_arch,
	'hw' : hw
}
testrun_form = TestRunForm(data=testrun)

if testrun_form.is_valid():
	testrun_obj = testrun_form.save(commit=False)
	if target in ["AB-Centos", "AB-Feodra", "AB-Opensuse", "AB-Ubuntu"]:
		testrun_obj.testplan = get_object_or_404(TestPlan, name="OE-Core master branch")
	else:
		testrun_obj.testplan = get_object_or_404(TestPlan, name="BSP/QEMU master branch")
	testrun_obj.save()
	print "TestRun saved"
else:
	print 'Error: TestRun json is not valid'
	sys.exit(1)


test_list = []
test_list_string = ""
test_id = result = msg = ""

if not os.path.isfile(log_file):
	print "Error: Cannot find log file"
	sys.exit(1)

with open(log_file, 'r') as content_file:
	content = content_file.read()

content = content.split("\n")

for i in xrange(len(content) - 1):
	msg = ""
	if (": PASSED" in content[i]) or (": FAILED" in content[i]):
		content[i] = content[i].split(" - Testcase ")[1]
		test_id = content[i].split(":")[0].lower().replace(" ", "")
		result = content[i].split(":")[1].lower().replace(" ", "")
		if result == "failed":
			for j in range(i + 2, len(content) - 1):
				if " - Testcase " not in content[j]: # TODO and (content[j] != ""):
					msg += content[j] + "\n"
				else:
					break

			msg = msg.replace('\"','\\\"')
			msg = msg.replace('\\\\', '(double backslash)')
			msg = msg.replace('\\_', ' ')
			msg = msg.strip('\\\\')
			msg = msg.replace('\\n\\n_', '\\n')
			msg = msg.replace('\t', ' ')

		testcaseresult = {
			"testcase_id" : test_id,
			"result" : result,
			"message" : msg
		}

		testcaseresult_form = TestCaseResultForm(data=testcaseresult)
		if testcaseresult_form.is_valid():
			testcaseresult_obj = testcaseresult_form.save(commit=False)
			testcaseresult_obj.testrun = testrun_obj
			testcaseresult_obj.save()
		else:
			print 'Error: A TestCaseResult json is not valid'
			sys.exit(1)

print "All TestCaseResults saved. Done"