import http.server
import socketserver
import json
import requests
from os import listdir
from os.path import isfile, join
import sys, os
import time
from datetime import datetime
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import random

import sys

#choose path where agent is
mypath = os.path.dirname(os.path.realpath(__file__))

print ("The script has the name %s" % (sys.argv[0]))
print ("The company key is %s" % (sys.argv[1]))
print ("The licence key is %s" % (sys.argv[2]))
print ("The authentication path is %s" % (sys.argv[3]))
print ("The get parser path is %s" % (sys.argv[4]))

#save company key
company = sys.argv[1]
#save licence key
licence = sys.argv[2]
#save auth path
AUTH_PATH = sys.argv[3]
#save parser path
GET_PARSER_PATH = sys.argv[4]

#send request for token
customer = {}
customer['method'] = "gettoken"
customer['companykey'] = company
customer['licensekey'] = licence
r = requests.post(AUTH_PATH, data=json.dumps(customer, ensure_ascii=False).encode('utf-8')) #gets token subscription service
data = r._content
body = json.loads(data)
token = body['token']
print("Got ID " + str(body))

#save ports to send logs to, one port for each code
ports = []
for i in range(5,len(sys.argv)):
    print(sys.argv[i])
    coderequest={}
    coderequest['token'] = token
    coderequest['parser_name'] = sys.argv[i]
    print(coderequest)
    r = requests.post(GET_PARSER_PATH, json=coderequest)
    print(r)
    data = r._content
    url = json.loads(data)
    #if code not ready to recieve logs yet, wait
    while url['IPs']== []:
        time.sleep(10)
        r = requests.post(GET_PARSER_PATH, json=coderequest)
        data = r._content
        url = json.loads(data)
    #if multiple ports for one code, choose one randomly
    IP = random.choice(url['IPs'])
    #save all IPs in a list
    ports.append(IP)

#load in all files in current path (that is not itself and is not .DS_Store, which is a mac-thing)
uploaded_files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f!='Agent.py' and f!='.DS_Store' ]

#print to terminal which files is within the folder 
print("Files in current folder is " + str(uploaded_files))

#function that composes token, file_content and timestamp
def post_content(file_name, token):
    open_file = open(file_name, 'r', encoding="utf-8")
    file_content = open_file.read()
    current_milli_time = int(round(time.time() * 1000))
    data = {}
    data['authorization'] = token
    data['timestamp'] = current_milli_time
    data['log'] = file_content
    #send logs to all codes chosen
    for i in range(len(ports)):
        r = requests.post(("http://" + ports[i] + "/submitLog"), json=data)

#data=json.dumps(data, ensure_ascii=False).encode('utf-8')
#'http://18.185.149.38:7999/submitLog'

#upload current files
for i in uploaded_files:
    post_content(i,token)

#function to find new logs
def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 

#always run agent
agent = True 
#continouesly send new logs
while agent == True: 
    current_files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f!='Agent.py' and f!='.DS_Store']
    if uploaded_files == current_files:
        time.sleep(10)
    else:
        new_files = Diff(current_files,uploaded_files)
        print(new_files)
        for i in new_files:
            post_content(i,token)
        uploaded_files = current_files

