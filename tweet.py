# -*- coding: utf-8 -*-
# tweet.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys

class TwitterTweet:
     def __init__(self):
         self.username = "Shunto Mizushima"
         self.password = "mizushima4105"
     
     def tweet(self):
 
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

         tweet = {
             "authenticity_token": "",
             "is_permalink_page": "false",
             "place_id": "",
             "status": "test",
             "tagged_users": ""
         }

         
         try: 
             response = session.get('https://twitter.com/', headers=headers, allow_redirects=False)
             soup = BeautifulSoup(response.text, "lxml")
             auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
         except ConnectionError:
             print "[*] Can't connect to Twitter."
             sys.exit()
 
         payload['authenticity_token'] = auth_token
         tweet['authenticity_token'] = auth_token
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
             
         try:
            tweet = session.post('https://twitter.com/i/tweet/create', data=tweet, allow_redirects=False, headers=headers, cookies=login.cookies)
            if tweet.status_code == 200:
                print "[+] Tweeted successfully, HTTP Status Code: %d" % tweet.status_code
            else:
                print "[+] Failed to tweet, HTTP Status Code: %d" % tweet.status_code
             
         except: 
            "[+] An error occurred in the middle of tweeting."
if __name__ == "__main__":
     TwiTweet = TwitterTweet()
     TwiTweet.tweet()                
