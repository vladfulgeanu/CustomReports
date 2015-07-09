#! /usr/bin/env python

# Command line utility that inserts a new Test Run and all its
# corresponding Test Case Results into the Test Reporting Tool's database.
# It does this by parsing a log file and getting all necessary Test Run
# details from given parameters.
# It assumes that the log file is in the same directory.
#
# Positional arguments:
#       - log file
#       - version (e.g "1.8")
#       - release (e.g "1.8_M2.rc2")
#       - test type - it accepts only two options, "Weekly" and "Full Pass"
#       - poky Git commit
#       - poky Git branch
#       - start date for the Test Run
#       - target (e.g "genericx86")
#       - image type (e.g. "core-image-sato")
#       - hardware architecture (e.g "x86")
#       - device on which the Test Run executed (e.g. "Atom-PC")
#
# It currently handles only two types of Test Plans: OE-Core and BSP.
# It chooses the corresponding Test Plan by checking the value of the "target"
# parameters.

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
    print "Example: python add_testrun.py results.log \"1.8\" \"1.8_rc1\" \"Weekly\" \"29812e61736a95f1de64b3e9ebbb9c646ebd28dd\" \"master\" \"2015-05-15 11:39:23\" \"genericx86\" \"core-image-sato\" \"x86_64\" \"NUC\""
    print "<start_date> _must_ respect the format in the example. <test_type> _must_ be either \"Weekly\" or \"Full Pass\""
    sys.exit(1)

testrun_obj = None

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
    if target in ["AB-Centos", "AB-Fedora", "AB-Opensuse", "AB-Ubuntu"]:
        # then Test Plan is "OE-Core"
        testrun_obj.testplan = get_object_or_404(TestPlan, name="OE-Core master branch")
    else:
        # then Test Plan is "BSP"
        testrun_obj.testplan = get_object_or_404(TestPlan, name="BSP/QEMU master branch")
    testrun_obj.save()
    print "TestRun saved"
else:
    print 'Error: TestRun json is not valid. Exiting ...'
    sys.exit(1)


test_list = []
test_list_string = ""
test_id = result = msg = ""

if not os.path.isfile(log_file):
    print "Error: Cannot find log file"
    testrun_obj.delete()
    print 'Test Run deleted. Exiting ...'
    sys.exit(1)

# Parse the log_file and create new instances of Test Case Results
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
                    if (" - Testcase " not in content[j]) and (content[j] != ""):
                        msg += content[j] + "\n"
                    else:
                        break

                msg = msg.replace('\"', '\\\"')
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
                testrun_obj.delete()
                print 'Test Run deleted. Exiting ...'
                sys.exit(1)

    print "All TestCaseResults saved. Done"
