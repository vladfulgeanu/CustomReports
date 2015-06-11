#!/usr/bin/python

import sys
import time
from time import gmtime, strftime
import datetime
import subprocess
from uuid import uuid4
import os.path


try:
  target = str(sys.argv[1])
  name = str(sys.argv[2])
  context = str(sys.argv[3])
  bsp_type = str(sys.argv[4])
  uid = str(uuid4())
  test_type = str(sys.argv[5])
  commit = str(sys.argv[6])
  build_date = str(sys.argv[7])
  img_type = str(sys.argv[8])
except IndexError, NameError:
	print "Usage: log2bundle <file> <name> <context> <bsp_type> <test_type> <commit> <date> <img_type> \n Example: log2bundle results-bitbake-worker.log runtime yocto-1.7.rc1 nuc weekly 8ac8eca2e3bd8c78e2b31ea974930ed0243258a3 2014-09-24 core-image-sato-sdk"
	exit(1)

year = time.strftime("%Y-%m-%e", gmtime())
hour = time.strftime("%H:%M:%S", gmtime())

test_list = []
test_list_string = ""
test_id = ""
result = ""
msg = ""

if not os.path.isfile(target):
  print "Cannot find log file!"
  exit(1)

with open(target, 'r') as content_file:
    content = content_file.read()

file_content = subprocess.check_output("echo \"%s\" | openssl enc -base64" % content, shell=True)

content = content.split("\n")    

for i in xrange (len(content)-1):
  msg = ""
  if (": PASSED" in content[i]) or (": FAILED" in content[i]):
    content[i] = content[i].split(" - RESULTS - ")[1]
    test_id = content[i].split(":")[0].lower().replace(" ","-")
    result = content[i].split(":")[1].lower()
    if result == " passed":
      result = "pass"
    if result ==" failed":
      result = "fail"
      for j in range(i+2, len(content)-1):
	if (" - RESULTS - " not in content[j]) and (content[j] != ""):
          msg += content[j]+"\\n"
        else:
          break

    msg = msg.replace('\"','\\\"')
    msg = msg.replace('\\\\', '(double backslash)')
    msg = msg.replace('\\_', ' ')
    msg = msg.strip('\\\\')
    msg = msg.replace('\\n\\n_', '\\n')
    msg = msg.replace('\t', ' ')

    test_template = """    {
          "result": "%s",
          "test_case_id": "%s",
          "message": "%s"
        },
  """ % (result, test_id, msg)
    test_list.append(test_template)

for i in xrange(len(test_list)):
	test_list_string += test_list[i]

test_list_string = test_list_string[:test_list_string.rfind('\n')]
test_list_string = test_list_string[:test_list_string.rfind(',')]
file_content = file_content.replace('\n', '')

json = """{
 "test_runs": [
    {
    "software_context": {
        "image": {
          "name": "%s"
        }
    },
    "test_results": [
    	%s
      ],
      "attributes": {
        "target": "%s",
        "commit": "%s",
        "date": "%s",
        "image type": "%s"
      },
      "attachments": [
      {
        "content": "%s",
        "pathname": "%s",
        "mime_type": "text/plain"
      }
      ],
      "analyzer_assigned_uuid": "%s",
      "analyzer_assigned_date": "%sT%sZ",
      "test_id": "%s-%s",
      "time_check_performed": false
    }],
  "format": "Dashboard Bundle Format 1.7"
}""" % (context,test_list_string ,bsp_type ,commit ,build_date, img_type, file_content ,name, uid, year, hour, bsp_type, test_type)

#print json
bundlename = name+"_"+bsp_type+"_"+test_type+"_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+".bundle"
with open(bundlename, 'w') as the_file:
    the_file.write(json)

transfer_file = subprocess.check_output("sudo scp "+bundlename+" root@10.237.112.80:/var/lib/lava/dispatcher/tmp/bundle_streams/runtime/", shell=True)
print transfer_file
if (bsp_type == "intel-core2-32"):
    bsp_type = "core2_32"
if (bsp_type == "intel-core2-32-lsb"):
    bsp_type = "core2_32_lsb"
if (bsp_type == "intel-corei7-64"):
    bsp_type = "corei7_64"
if (bsp_type == "intel-corei7-64-lsb"):
    bsp_type = "corei7_64_lsb"
submit_file = subprocess.check_output("sudo ssh root@10.237.112.80 \"cd /var/lib/lava/dispatcher/tmp/bundle_streams/runtime/ && lava-tool put --dashboard-url=http://localhost/RPC2/ "+bundlename+" /anonymous/"+test_type+"-"+name+"-"+bsp_type+"/\"", shell=True)
print submit_file
analyze_bundle = subprocess.check_output("sudo ssh root@10.237.112.80 \"/var/lib/lava/dispatcher/tmp/bundle_streams/bundle_compare.py "+bsp_type+" "+test_type+" "+name+" "+build_date+" /var/lib/lava/dispatcher/tmp/bundle_streams\"", shell=True)
print analyze_bundle
