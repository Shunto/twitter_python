# -*- coding: utf-8 -*-
# login.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys

class TwitterLogin:
    def __init__(self):
        self.username = "Shunto Mizushima"
        self.password = "mizushima4105"
    
    def login(self):

        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://twitter.com/",
            "Origin": "https://twitter.com",
            "Upgrade-insecure-requests": "1"
        }

        payload = {
            "session[username_or_email]": "",
            "sesssion[password]": "",
            "remember_me": "1",
            "return_to_ssl": "",
            "redirect_after_login": "/",
            "scribe_log": ""
        }
        
        try: 
            response = session.get('https://twitter.com/', headers=headers, allow_redirects=False)
            soup = BeautifulSoup(response.text, "lxml")
            auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        except ConnectionError:
            print "[*] Can't connect to Twitter."
            sys.exit()

        payload['authenticity_token'] = auth_token
        payload['session[username_or_email]'] = self.username
        payload['session[password]'] = self.password

        try:
            login = session.post('https://twitter.com/sessions', headers=headers, data=payload, allow_redirects=False)
            if login.status_code == 302 or login.status_code == 200:
                print "[+] Loggined successfully, HTTP Status Code: %d" % login.status_code
            else:
                print "[+] Failed to loggin, HTTP Status Code: %d" % login.status_code
            
        except:
            "[+] An error occurred in the middle of the login."
            
if __name__ == "__main__":
    TwiLogin = TwitterLogin()
    TwiLogin.login()                
