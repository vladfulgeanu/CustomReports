#! /usr/bin/env python

# Command line utility that inserts a new Test Plan into the
# Test Reporting Tool's database.
#
# Positional arguments:
#       - name of the TestPlan (e.g. "BSP/QEMU master branch")
#       - name of the TestPlan's product (e.g. "BSPs")
#       - version (e.g "1.8")

import os, sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), "customreports/"))
os.environ["DJANGO_SETTINGS_MODULE"] = "customreports.settings"

django.setup()

from charts.models import TestPlanForm

try:
    name = str(sys.argv[1])
    product = str(sys.argv[2])
    product_version = str(sys.argv[3])
except IndexError, NameError:
    print "Usage: add_testplan \"<name>\" \"<product>\" \"<product_version>\""
    print "Example: python add_testplan.py \"BSP/QEMU master branch\" \"BSPs\" \"1.8\""
    sys.exit(1)


testplan = {
    'name' : name,
    'product' : product,
    'product_version' : product_version
    }

testplan_form = TestPlanForm(data=testplan)

if testplan_form.is_valid():
    testplan_obj = testplan_form.save()
    print "TestPlan saved"
else:
    print 'Error: TestPlan json is not valid'
    sys.exit(1)
