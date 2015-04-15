#! /usr/bin/env python

import json
import os, sys
import django

# Takes a .bundle file as argument
if len(sys.argv) != 2:
	print "Usage: json_deserializer.py <.bundle_file>"
 

sys.path.append(os.path.join(os.path.dirname(__file__), "customreports/"))
os.environ["DJANGO_SETTINGS_MODULE"] = "customreports.settings"

django.setup()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customreports.settings")
from charts.models import TestRunForm, TestResultForm

# open json arg file
json_file = open(sys.argv[1])
json_file_data = json.load(json_file)

# From the loaded json file construct a custom dictionary that will represent a TestRun DB entry
testrun_raw = json_file_data["test_runs"][0]

testrun = {}
testrun["target"] = testrun_raw["attributes"]["target"]
testrun["commit"] = testrun_raw["attributes"]["commit"]
testrun["date"] = testrun_raw["attributes"]["date"]
testrun["image_type"] = testrun_raw["attributes"]["image type"]

testrun_form = TestRunForm(data=testrun)

if testrun_form.is_valid():
	testrun_obj = testrun_form.save()

	# The raw TestResult json respects the model structure, so we don't need to create a new one
	for index, testresult_raw in enumerate(testrun_raw["test_results"]):
		testresult_form = TestResultForm(data=testresult_raw)

		if testresult_form.is_valid():
			testresult_obj = testresult_form.save(commit=False)
			testresult_obj.testrun = testrun_obj
			testresult_obj.save()
		else:
			print 'Error: The ' + `index` + 'th TestResult custom dictionary is not valid'
			sys.exit(1)

else:
	print 'Error: TestRun custom dictionary is not valid'
	sys.exit(1)
