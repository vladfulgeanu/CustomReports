#! /usr/bin/env python

import json
import os, sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), "customreports/"))
os.environ["DJANGO_SETTINGS_MODULE"] = "customreports.settings"

django.setup()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customreports.settings")
from charts.models import TestPlanForm, TestRunForm, TestCaseForm, TestCaseResultForm, TestReportForm

testreport = {
	'filters' : '{"release" : "1.7.2_rc3"}',
}

testreport_form = TestReportForm(data=testreport)

if testreport_form.is_valid():
	testreport_obj = testreport_form.save()
	print 'TRep1 saved'
else:
	print 'Error: TestReport json is not valid'
	sys.exit(1)


testplan = {
	'name' : 'BSP/QEMU: master branch',
	'product' : 'BSPs',
	'product_version' : '1.8',
	'created' : '2015-01-07 09:16:42',
	'author' : "Andreea Brandusa Proca <andreea.b.proca@intel.com>",
	'version' : '1',
	'plan_type' : 'Function',
}
testplan_form = TestPlanForm(data=testplan)

if testplan_form.is_valid():
	testplan_obj = testplan_form.save()
	print "TP1 saved"
else:
	print 'Error: TestPlan json is not valid'
	sys.exit(1)

testplan2 = {}

testplan2["name"] = "BSP/QEMU: danny branch"
testplan2["product"] = "BSPs"
testplan2["product_version"] = "1.8"
testplan2["created"] = "2013-01-11 17:23:06"
testplan2["author"] = "Stoicescu Cornel <corneliux.stoicescu@intel.com>"
testplan2["version"] = "2"
testplan2["plan_type"] = "Function"

testplan_form2 = TestPlanForm(data=testplan2)

if testplan_form2.is_valid():
	testplan_obj2 = testplan_form2.save()
	print "TP2 saved"

else:
	print 'Error: TestPlan2 json is not valid'
	sys.exit(1)



##############################

testrun = {
	"testrun_id" : "1245",
	"release" : "1.7.2_rc3",
	"test_type"  : "Weekly",
	"poky_commit" : "29812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-05 11:23:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "sugarbay"
}

testrun2 = {
	"testrun_id" : "3245",
	"release" : "1.7.2_rc3",
	"test_type"  : "Weekly",
	"poky_commit" : "29812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-15 11:39:23",
	"target" : "NUC",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "NUC"
}

testrun3 = {
	"testrun_id" : "2123",
	"release" : "1.7.2_rc3",
	"test_type"  : "Full Pass",
	"poky_commit" : "29812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-25 11:39:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "Atom-PC"
}

testrun_form = TestRunForm(data=testrun)

if testrun_form.is_valid():
	testrun_obj = testrun_form.save(commit=False)
	testrun_obj.testplan = testplan_obj
	testrun_obj.save()
	print "TR1 saved"

else:
	print 'Error: TestRun json is not valid'
	sys.exit(1)

testrun_form2 = TestRunForm(data=testrun2)

if testrun_form2.is_valid():
	testrun_obj2 = testrun_form2.save(commit=False)
	testrun_obj2.testplan = testplan_obj
	testrun_obj2.save()
	print "TR2 saved"

else:
	print 'Error: TestRun2 json is not valid'
	sys.exit(1)

testrun_form3 = TestRunForm(data=testrun3)

if testrun_form3.is_valid():
	testrun_obj3 = testrun_form3.save(commit=False)
	testrun_obj3.testplan = testplan_obj
	testrun_obj3.save()
	print "TR3 saved"

else:
	print 'Error: TestRun3 json is not valid'
	sys.exit(1)


##############################

testrun4 = {
	"testrun_id" : "1795",
	"release" : "1.7.2_rc4",
	"test_type"  : "Weekly",
	"poky_commit" : "32812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-26 11:23:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "sugarbay"
}

testrun5 = {
	"testrun_id" : "6537",
	"release" : "1.7.2_rc4",
	"test_type"  : "Weekly",
	"poky_commit" : "32812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-26 11:39:23",
	"target" : "NUC",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "NUC"
}

testrun6 = {
	"testrun_id" : "4724",
	"release" : "1.7.2_rc4",
	"test_type"  : "Full Pass",
	"poky_commit" : "32812e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-05-26 11:39:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "Atom-PC"
}

testrun_form4 = TestRunForm(data=testrun4)

if testrun_form4.is_valid():
	testrun_obj4 = testrun_form4.save(commit=False)
	testrun_obj4.testplan = testplan_obj
	testrun_obj4.save()
	print "TR4 saved"

else:
	print 'Error: TestRun4 json is not valid'
	sys.exit(1)

testrun_form5 = TestRunForm(data=testrun5)

if testrun_form5.is_valid():
	testrun_obj5 = testrun_form5.save(commit=False)
	testrun_obj5.testplan = testplan_obj
	testrun_obj5.save()
	print "TR5 saved"

else:
	print 'Error: TestRun5 json is not valid'
	sys.exit(1)

testrun_form6 = TestRunForm(data=testrun6)

if testrun_form6.is_valid():
	testrun_obj6 = testrun_form6.save(commit=False)
	testrun_obj6.testplan = testplan_obj
	testrun_obj6.save()
	print "TR6 saved"

else:
	print 'Error: TestRun6 json is not valid'
	sys.exit(1)

##############################

testcase1 = {
	"testcase_id" : "215",
	"summary" : "do important thinggy",
	"author" : "Stoicescu Cornel <corneliux.stoicescu@intel.com>",
	"tester" : "Stoicescu Cornel <corneliux.stoicescu@intel.com>",
	"category" : "Weekly",
	"priority" : "High"
}

testcase2 = {
	"testcase_id" : "285",
	"summary" : "do other thinggy then do that",
	"author" : "Stoicescu Cornel <corneliux.stoicescu@intel.com>",
	"tester" : "Stoicescu Cornel <corneliux.stoicescu@intel.com>",
	"category" : "Weekly",
	"priority" : "Medium"
}

testcase_form1 = TestCaseForm(data=testcase1)

if testcase_form1.is_valid():
	testcase_obj1 = testcase_form1.save(commit=False)
	testcase_obj1.testplan = testplan_obj
	testcase_obj1.save()
	print "TC1 saved"

else:
	print 'Error: TestCase1 json is not valid'
	sys.exit(1)

testcase_form2 = TestCaseForm(data=testcase2)

if testcase_form2.is_valid():
	testcase_obj2 = testcase_form2.save(commit=False)
	testcase_obj2.testplan = testplan_obj
	testcase_obj2.save()
	print "TC2 saved"

else:
	print 'Error: TestCase2 json is not valid'
	sys.exit(1)

##############################
testcaseresult1 = {
	"result" : "fail",
	"started_on" : "2015-05-17 11:39:23",
	"finished_on" : "2015-05-17 11:54:23"
}

testcaseresult2 = {
	"result" : "pass",
	"started_on" : "2015-05-05 11:23:23",
	"finished_on" : "2015-05-05 11:24:23"
}


testcaseres_form1 = TestCaseResultForm(data=testcaseresult1)

if testcaseres_form1.is_valid():
	testcaseres_obj1 = testcaseres_form1.save(commit=False)
	testcaseres_obj1.testcase = testcase_obj1
	testcaseres_obj1.testrun = testrun_obj
	testcaseres_obj1.save()
	print 'TCR1 saved'

else:
	print 'Error: TestCaseRes1 json is not valid'
	sys.exit(1)

testcaseres_form2 = TestCaseResultForm(data=testcaseresult2)

if testcaseres_form2.is_valid():
	testcaseres_obj2 = testcaseres_form2.save(commit=False)
	testcaseres_obj2.testcase = testcase_obj2
	testcaseres_obj2.testrun = testrun_obj
	testcaseres_obj2.save()
	print 'TCR2 saved'

else:
	print 'Error: TestCaseRes2 json is not valid'
	sys.exit(1)


testcaseresult3 = {
	"result" : "fail",
	"started_on" : "2015-05-18 11:39:23",
	"finished_on" : "2015-05-18 11:54:23"
}

testcaseresult4 = {
	"result" : "pass",
	"started_on" : "2015-05-15 11:23:23",
	"finished_on" : "2015-05-15 11:24:23"
}


testcaseres_form3 = TestCaseResultForm(data=testcaseresult3)

if testcaseres_form3.is_valid():
	testcaseres_obj3 = testcaseres_form3.save(commit=False)
	testcaseres_obj3.testcase = testcase_obj1
	testcaseres_obj3.testrun = testrun_obj2
	testcaseres_obj3.save()
	print 'TCR3 saved'

else:
	print 'Error: TestCaseRes3 json is not valid'
	sys.exit(1)

testcaseres_form4 = TestCaseResultForm(data=testcaseresult4)

if testcaseres_form4.is_valid():
	testcaseres_obj4 = testcaseres_form4.save(commit=False)
	testcaseres_obj4.testcase = testcase_obj2
	testcaseres_obj4.testrun = testrun_obj2
	testcaseres_obj4.save()
	print 'TCR4 saved'

else:
	print 'Error: TestCaseRes4 json is not valid'
	sys.exit(1)

testcaseresult5 = {
	"result" : "pass",
	"started_on" : "2015-05-21 11:39:23",
	"finished_on" : "2015-05-21 11:54:23"
}

testcaseresult6 = {
	"result" : "pass",
	"started_on" : "2015-05-25 11:23:23",
	"finished_on" : "2015-05-25 11:24:23"
}


testcaseres_form5 = TestCaseResultForm(data=testcaseresult5)

if testcaseres_form5.is_valid():
	testcaseres_obj5 = testcaseres_form5.save(commit=False)
	testcaseres_obj5.testcase = testcase_obj1
	testcaseres_obj5.testrun = testrun_obj3
	testcaseres_obj5.save()
	print 'TCR5 saved'

else:
	print 'Error: TestCaseRes5 json is not valid'
	sys.exit(1)

testcaseres_form6 = TestCaseResultForm(data=testcaseresult6)

if testcaseres_form6.is_valid():
	testcaseres_obj6 = testcaseres_form6.save(commit=False)
	testcaseres_obj6.testcase = testcase_obj2
	testcaseres_obj6.testrun = testrun_obj3
	testcaseres_obj6.save()
	print 'TCR6 saved'

else:
	print 'Error: TestCaseRes6 json is not valid'
	sys.exit(1)


##############################
testcaseresult7 = {
	"result" : "fail",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult8 = {
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form7 = TestCaseResultForm(data=testcaseresult7)

if testcaseres_form7.is_valid():
	testcaseres_obj7 = testcaseres_form7.save(commit=False)
	testcaseres_obj7.testcase = testcase_obj1
	testcaseres_obj7.testrun = testrun_obj4
	testcaseres_obj7.save()
	print 'TCR7 saved'

else:
	print 'Error: TestCaseRes7 json is not valid'
	sys.exit(1)

testcaseres_form8 = TestCaseResultForm(data=testcaseresult8)

if testcaseres_form8.is_valid():
	testcaseres_obj8 = testcaseres_form8.save(commit=False)
	testcaseres_obj8.testcase = testcase_obj2
	testcaseres_obj8.testrun = testrun_obj4
	testcaseres_obj8.save()
	print 'TCR8 saved'

else:
	print 'Error: TestCaseRes8 json is not valid'
	sys.exit(1)


testcaseresult9 = {
	"result" : "fail",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult10 = {
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form9 = TestCaseResultForm(data=testcaseresult9)

if testcaseres_form9.is_valid():
	testcaseres_obj9 = testcaseres_form9.save(commit=False)
	testcaseres_obj9.testcase = testcase_obj1
	testcaseres_obj9.testrun = testrun_obj5
	testcaseres_obj9.save()
	print 'TCR9 saved'

else:
	print 'Error: TestCaseRes9 json is not valid'
	sys.exit(1)

testcaseres_form10 = TestCaseResultForm(data=testcaseresult10)

if testcaseres_form10.is_valid():
	testcaseres_obj10 = testcaseres_form10.save(commit=False)
	testcaseres_obj10.testcase = testcase_obj2
	testcaseres_obj10.testrun = testrun_obj5
	testcaseres_obj10.save()
	print 'TCR10 saved'

else:
	print 'Error: TestCaseRes10 json is not valid'
	sys.exit(1)

testcaseresult11 = {
	"result" : "pass",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult12 = {
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form11 = TestCaseResultForm(data=testcaseresult11)

if testcaseres_form11.is_valid():
	testcaseres_obj11 = testcaseres_form11.save(commit=False)
	testcaseres_obj11.testcase = testcase_obj1
	testcaseres_obj11.testrun = testrun_obj6
	testcaseres_obj11.save()
	print 'TCR11 saved'

else:
	print 'Error: TestCaseRes11 json is not valid'
	sys.exit(1)

testcaseres_form12 = TestCaseResultForm(data=testcaseresult12)

if testcaseres_form12.is_valid():
	testcaseres_obj12 = testcaseres_form12.save(commit=False)
	testcaseres_obj12.testcase = testcase_obj2
	testcaseres_obj12.testrun = testrun_obj6
	testcaseres_obj12.save()
	print 'TCR12 saved'

else:
	print 'Error: TestCaseRes12 json is not valid'
	sys.exit(1)

#############################################
"""
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
"""