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

#choose path where agent is
mypath = os.path.dirname(os.path.realpath(__file__))

#load in all files in current path
uploaded_files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f!='Agent.py' and f!='.DS_Store' ]

#print to terminal which files is within the folder 
print("Files in current folder is " + str(uploaded_files))

#send GET request for token
r = requests.get('http://localhost:8000')
data = r._content
token = json.loads(data)
token = token['ID']
print("Got token " + str(token))

#Agent token - where does it come from?? 
#token = "42"

#function that composes token, file_content and timestamp
def post_content(file_name, token):
    open_file = open(file_name, 'r', encoding="utf-8")
    file_content = open_file.read()
    current_milli_time = int(round(time.time() * 1000))
    data = {}
    data['agent'] = token
    data['timestamp'] = current_milli_time
    data['log'] = file_content
    r = requests.post('http://localhost:8000', data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

#data=json.dumps(data, ensure_ascii=False).encode('utf-8')
#'http://18.185.149.38:7999/submitLog'

for i in uploaded_files:
    post_content(i,token)

agent = True 

def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 

while agent == True: 
    current_files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f!='Agent.py' and f!='.DS_Store']
    if uploaded_files == current_files:
        time.sleep(10)
    else:
        print(current_files)

        new_files = Diff(current_files,uploaded_files)

        for i in new_files:
            post_content(i,token)
        
        uploaded_files = current_files

