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

#choose path where agent is
mypath = os.path.dirname(os.path.realpath(__file__))

#load in all files in current path
uploaded_files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f!='Agent.py' and f!='.DS_Store' ]

#print to terminal which files is within the folder 
print("Files in current folder is " + str(uploaded_files))

#send GET request for token
r = requests.get('http://localhost:8000') #gets token subscription service
data = r._content
token = json.loads(data)
ID = token['ID']
print("Got ID " + str(token))

#send GET request for URL+port
r = requests.get('http://localhost:8000') #gets from parser execute 
data = r._content
url = json.loads(data)
IP = random.choice(url['IPs'])
print("Got IP " + str(IP))

#function that composes token, file_content and timestamp
def post_content(file_name, token):
    open_file = open(file_name, 'r', encoding="utf-8")
    file_content = open_file.read()
    current_milli_time = int(round(time.time() * 1000))
    data = {}
    data['agent'] = ID
    data['timestamp'] = current_milli_time
    data['log'] = file_content
    r = requests.post(IP, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

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
        new_files = Diff(current_files,uploaded_files)
        print(new_files)
        for i in new_files:
            post_content(i,token)
        
        uploaded_files = current_files

