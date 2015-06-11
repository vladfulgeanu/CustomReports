#! /usr/bin/env python

import json
import os, sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), "customreports/"))
os.environ["DJANGO_SETTINGS_MODULE"] = "customreports.settings"

django.setup()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customreports.settings")
from charts.models import TestPlanForm, TestRunForm, TestCaseResultForm, TestReportForm

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
	"version" : "1.7",
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
	"version" : "1.7",
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
	"version" : "1.7",
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
	"version" : "1.7",
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
	"version" : "1.7",
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
	"version" : "1.7",
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

testrun7 = {
	"testrun_id" : "2895",
	"version" : "1.7",
	"release" : "1.7.2_rc2",
	"test_type"  : "Weekly",
	"poky_commit" : "gyh12e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-04-26 11:23:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "sugarbay"
}

testrun8 = {
	"testrun_id" : "4391",
	"version" : "1.7",
	"release" : "1.7.2_rc2",
	"test_type"  : "Weekly",
	"poky_commit" : "gyh12e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-04-26 11:39:23",
	"target" : "NUC",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "NUC"
}

testrun9 = {
	"testrun_id" : "3528",
	"version" : "1.7",
	"release" : "1.7.2_rc2",
	"test_type"  : "Full Pass",
	"poky_commit" : "gyh12e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-04-26 11:39:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "Atom-PC"
}

testrun_form7 = TestRunForm(data=testrun7)

if testrun_form7.is_valid():
	testrun_obj7 = testrun_form7.save(commit=False)
	testrun_obj7.testplan = testplan_obj
	testrun_obj7.save()
	print "TR7 saved"

else:
	print 'Error: TestRun7 json is not valid'
	sys.exit(1)

testrun_form8 = TestRunForm(data=testrun8)

if testrun_form8.is_valid():
	testrun_obj8 = testrun_form8.save(commit=False)
	testrun_obj8.testplan = testplan_obj
	testrun_obj8.save()
	print "TR8 saved"

else:
	print 'Error: TestRun8 json is not valid'
	sys.exit(1)

testrun_form9 = TestRunForm(data=testrun9)

if testrun_form9.is_valid():
	testrun_obj9 = testrun_form9.save(commit=False)
	testrun_obj9.testplan = testplan_obj
	testrun_obj9.save()
	print "TR9 saved"

else:
	print 'Error: TestRun9 json is not valid'
	sys.exit(1)

##############################

testrun10 = {
	"testrun_id" : "3457",
	"version" : "1.8",
	"release" : "1.8_rc1",
	"test_type"  : "Full Pass",
	"poky_commit" : "fgh12e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-06-10 11:39:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "Atom-PC"
}

testrun_form10 = TestRunForm(data=testrun10)

if testrun_form10.is_valid():
	testrun_obj10 = testrun_form10.save(commit=False)
	testrun_obj10.testplan = testplan_obj
	testrun_obj10.save()
	print "TR10 saved"

else:
	print 'Error: TestRun10 json is not valid'
	sys.exit(1)


testrun11 = {
	"testrun_id" : "6932",
	"version" : "1.7",
	"release" : "1.7.2_rc2",
	"test_type"  : "Full Pass",
	"poky_commit" : "tg312e61736a95f1de64b3e9ebbb9c646ebd28dd",
	"poky_branch" : "dizzy",
	"date" : "2015-04-27 11:39:23",
	"target" : "genericx86",
	"image_type" : "core-image-sato",
	"hw_arch" : "x86_64",
	"hw" : "Atom-PC"
}

testrun_form11 = TestRunForm(data=testrun11)

if testrun_form11.is_valid():
	testrun_obj11 = testrun_form11.save(commit=False)
	testrun_obj11.testplan = testplan_obj
	testrun_obj11.save()
	print "TR11 saved"

else:
	print 'Error: TestRun11 json is not valid'
	sys.exit(1)


#################################
testcaseresult1 = {
	"testcase_id" : "215",
	"result" : "fail",
	"started_on" : "2015-05-17 11:39:23",
	"finished_on" : "2015-05-17 11:54:23"
}

testcaseresult2 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-05 11:23:23",
	"finished_on" : "2015-05-05 11:24:23"
}


testcaseres_form1 = TestCaseResultForm(data=testcaseresult1)

if testcaseres_form1.is_valid():
	testcaseres_obj1 = testcaseres_form1.save(commit=False)
	testcaseres_obj1.testrun = testrun_obj
	testcaseres_obj1.save()
	print 'TCR1 saved'

else:
	print 'Error: TestCaseRes1 json is not valid'
	sys.exit(1)

testcaseres_form2 = TestCaseResultForm(data=testcaseresult2)

if testcaseres_form2.is_valid():
	testcaseres_obj2 = testcaseres_form2.save(commit=False)
	testcaseres_obj2.testrun = testrun_obj
	testcaseres_obj2.save()
	print 'TCR2 saved'

else:
	print 'Error: TestCaseRes2 json is not valid'
	sys.exit(1)


testcaseresult3 = {
	"testcase_id" : "215",
	"result" : "fail",
	"started_on" : "2015-05-18 11:39:23",
	"finished_on" : "2015-05-18 11:54:23"
}

testcaseresult4 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-15 11:23:23",
	"finished_on" : "2015-05-15 11:24:23"
}


testcaseres_form3 = TestCaseResultForm(data=testcaseresult3)

if testcaseres_form3.is_valid():
	testcaseres_obj3 = testcaseres_form3.save(commit=False)
	testcaseres_obj3.testrun = testrun_obj2
	testcaseres_obj3.save()
	print 'TCR3 saved'

else:
	print 'Error: TestCaseRes3 json is not valid'
	sys.exit(1)

testcaseres_form4 = TestCaseResultForm(data=testcaseresult4)

if testcaseres_form4.is_valid():
	testcaseres_obj4 = testcaseres_form4.save(commit=False)
	testcaseres_obj4.testrun = testrun_obj2
	testcaseres_obj4.save()
	print 'TCR4 saved'

else:
	print 'Error: TestCaseRes4 json is not valid'
	sys.exit(1)

testcaseresult5 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-05-21 11:39:23",
	"finished_on" : "2015-05-21 11:54:23"
}

testcaseresult6 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-25 11:23:23",
	"finished_on" : "2015-05-25 11:24:23"
}


testcaseres_form5 = TestCaseResultForm(data=testcaseresult5)

if testcaseres_form5.is_valid():
	testcaseres_obj5 = testcaseres_form5.save(commit=False)
	testcaseres_obj5.testrun = testrun_obj3
	testcaseres_obj5.save()
	print 'TCR5 saved'

else:
	print 'Error: TestCaseRes5 json is not valid'
	sys.exit(1)

testcaseres_form6 = TestCaseResultForm(data=testcaseresult6)

if testcaseres_form6.is_valid():
	testcaseres_obj6 = testcaseres_form6.save(commit=False)
	testcaseres_obj6.testrun = testrun_obj3
	testcaseres_obj6.save()
	print 'TCR6 saved'

else:
	print 'Error: TestCaseRes6 json is not valid'
	sys.exit(1)


##############################
testcaseresult7 = {
	"testcase_id" : "215",
	"result" : "fail",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult8 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form7 = TestCaseResultForm(data=testcaseresult7)

if testcaseres_form7.is_valid():
	testcaseres_obj7 = testcaseres_form7.save(commit=False)
	testcaseres_obj7.testrun = testrun_obj4
	testcaseres_obj7.save()
	print 'TCR7 saved'

else:
	print 'Error: TestCaseRes7 json is not valid'
	sys.exit(1)

testcaseres_form8 = TestCaseResultForm(data=testcaseresult8)

if testcaseres_form8.is_valid():
	testcaseres_obj8 = testcaseres_form8.save(commit=False)
	testcaseres_obj8.testrun = testrun_obj4
	testcaseres_obj8.save()
	print 'TCR8 saved'

else:
	print 'Error: TestCaseRes8 json is not valid'
	sys.exit(1)


testcaseresult9 = {
	"testcase_id" : "215",
	"result" : "fail",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult10 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form9 = TestCaseResultForm(data=testcaseresult9)

if testcaseres_form9.is_valid():
	testcaseres_obj9 = testcaseres_form9.save(commit=False)
	testcaseres_obj9.testrun = testrun_obj5
	testcaseres_obj9.save()
	print 'TCR9 saved'

else:
	print 'Error: TestCaseRes9 json is not valid'
	sys.exit(1)

testcaseres_form10 = TestCaseResultForm(data=testcaseresult10)

if testcaseres_form10.is_valid():
	testcaseres_obj10 = testcaseres_form10.save(commit=False)
	testcaseres_obj10.testrun = testrun_obj5
	testcaseres_obj10.save()
	print 'TCR10 saved'

else:
	print 'Error: TestCaseRes10 json is not valid'
	sys.exit(1)

testcaseresult11 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-05-26 11:39:23",
	"finished_on" : "2015-05-26 11:54:23"
}

testcaseresult12 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-05-26 11:23:23",
	"finished_on" : "2015-05-26 11:24:23"
}


testcaseres_form11 = TestCaseResultForm(data=testcaseresult11)

if testcaseres_form11.is_valid():
	testcaseres_obj11 = testcaseres_form11.save(commit=False)
	testcaseres_obj11.testrun = testrun_obj6
	testcaseres_obj11.save()
	print 'TCR11 saved'

else:
	print 'Error: TestCaseRes11 json is not valid'
	sys.exit(1)

testcaseres_form12 = TestCaseResultForm(data=testcaseresult12)

if testcaseres_form12.is_valid():
	testcaseres_obj12 = testcaseres_form12.save(commit=False)
	testcaseres_obj12.testrun = testrun_obj6
	testcaseres_obj12.save()
	print 'TCR12 saved'

else:
	print 'Error: TestCaseRes12 json is not valid'
	sys.exit(1)


##############################
testcaseresult13 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-04-26 11:39:23",
	"finished_on" : "2015-04-26 11:54:23"
}

testcaseresult14 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-04-26 11:23:23",
	"finished_on" : "2015-04-26 11:24:23"
}


testcaseres_form13 = TestCaseResultForm(data=testcaseresult13)

if testcaseres_form13.is_valid():
	testcaseres_obj13 = testcaseres_form13.save(commit=False)
	testcaseres_obj13.testrun = testrun_obj7
	testcaseres_obj13.save()
	print 'TCR13 saved'

else:
	print 'Error: TestCaseRes13 json is not valid'
	sys.exit(1)

testcaseres_form14 = TestCaseResultForm(data=testcaseresult14)

if testcaseres_form14.is_valid():
	testcaseres_obj14 = testcaseres_form14.save(commit=False)
	testcaseres_obj14.testrun = testrun_obj7
	testcaseres_obj14.save()
	print 'TCR14 saved'

else:
	print 'Error: TestCaseRes14 json is not valid'
	sys.exit(1)


testcaseresult15 = {
	"testcase_id" : "215",
	"result" : "fail",
	"started_on" : "2015-04-26 11:39:23",
	"finished_on" : "2015-04-26 11:54:23"
}

testcaseresult16 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-04-26 11:23:23",
	"finished_on" : "2015-04-26 11:24:23"
}


testcaseres_form15 = TestCaseResultForm(data=testcaseresult15)

if testcaseres_form15.is_valid():
	testcaseres_obj9 = testcaseres_form15.save(commit=False)
	testcaseres_obj9.testrun = testrun_obj8
	testcaseres_obj9.save()
	print 'TCR15 saved'

else:
	print 'Error: TestCaseRes15 json is not valid'
	sys.exit(1)

testcaseres_form16 = TestCaseResultForm(data=testcaseresult16)

if testcaseres_form16.is_valid():
	testcaseres_obj16 = testcaseres_form16.save(commit=False)
	testcaseres_obj16.testrun = testrun_obj8
	testcaseres_obj16.save()
	print 'TCR16 saved'

else:
	print 'Error: TestCaseRes16 json is not valid'
	sys.exit(1)

testcaseresult17 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-04-26 11:39:23",
	"finished_on" : "2015-04-26 11:54:23"
}

testcaseresult18 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-04-26 11:23:23",
	"finished_on" : "2015-04-26 11:24:23"
}


testcaseres_form17 = TestCaseResultForm(data=testcaseresult17)

if testcaseres_form17.is_valid():
	testcaseres_obj17 = testcaseres_form17.save(commit=False)
	testcaseres_obj17.testrun = testrun_obj9
	testcaseres_obj17.save()
	print 'TCR17 saved'

else:
	print 'Error: TestCaseRes17 json is not valid'
	sys.exit(1)

testcaseres_form18 = TestCaseResultForm(data=testcaseresult18)

if testcaseres_form18.is_valid():
	testcaseres_obj18 = testcaseres_form18.save(commit=False)
	testcaseres_obj18.testrun = testrun_obj9
	testcaseres_obj18.save()
	print 'TCR18 saved'

else:
	print 'Error: TestCaseRes18 json is not valid'
	sys.exit(1)
##############################
testcaseresult19 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-06-10 11:39:23",
	"finished_on" : "2015-06-10 11:54:23"
}

testcaseresult20 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-06-10 11:23:23",
	"finished_on" : "2015-06-10 11:24:23"
}


testcaseres_form19 = TestCaseResultForm(data=testcaseresult19)

if testcaseres_form19.is_valid():
	testcaseres_obj19 = testcaseres_form19.save(commit=False)
	testcaseres_obj19.testrun = testrun_obj10
	testcaseres_obj19.save()
	print 'TCR19 saved'

else:
	print 'Error: TestCaseRes19 json is not valid'
	sys.exit(1)

testcaseres_form20 = TestCaseResultForm(data=testcaseresult20)

if testcaseres_form20.is_valid():
	testcaseres_obj20 = testcaseres_form20.save(commit=False)
	testcaseres_obj20.testrun = testrun_obj10
	testcaseres_obj20.save()
	print 'TCR20 saved'

else:
	print 'Error: TestCaseRes20 json is not valid'
	sys.exit(1)


testcaseresult21 = {
	"testcase_id" : "215",
	"result" : "pass",
	"started_on" : "2015-04-27 11:39:23",
	"finished_on" : "2015-04-27 11:54:23"
}

testcaseresult22 = {
	"testcase_id" : "216",
	"result" : "pass",
	"started_on" : "2015-04-27 11:23:23",
	"finished_on" : "2015-04-27 11:24:23"
}


testcaseres_form21 = TestCaseResultForm(data=testcaseresult21)

if testcaseres_form21.is_valid():
	testcaseres_obj21 = testcaseres_form21.save(commit=False)
	testcaseres_obj21.testrun = testrun_obj11
	testcaseres_obj21.save()
	print 'TCR21 saved'

else:
	print 'Error: TestCaseRes21 json is not valid'
	sys.exit(1)

testcaseres_form22 = TestCaseResultForm(data=testcaseresult22)

if testcaseres_form22.is_valid():
	testcaseres_obj22 = testcaseres_form22.save(commit=False)
	testcaseres_obj22.testrun = testrun_obj11
	testcaseres_obj22.save()
	print 'TCR22 saved'

else:
	print 'Error: TestCaseRes22 json is not valid'
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