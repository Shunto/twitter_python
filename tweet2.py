# -*- coding: utf-8 -*-
# tweet2.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys

class TwitterTweet:
     def __init__(self):
         self.username = "Shunto Mizushima"
         self.password = "mizushima4105"
         self.host_url = "https://twitter.com/"
         self.mypage_url = self.host_url + self.username
         self.session_url = self.host_url + "sessions"
         self.tweet_url = self.host_url + "i/tweet/create" 
         self.destroy_url = self.host_url + "i/tweet/destroy"
     
     def tweet(self):
 
         session = requests.Session()
 
         headers = {
             "User-Agent": "Mozilla/5.0",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
             "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
             "Content-Type": "application/x-www-form-urlencoded",
             "Referer": "https://twitter.com/",
             "Origin": "https://twitter.com",
             "Upgrade-insecure-requests": "1",
             "X-Twitter-Active-User": "no",
             #"X-Requested-With": "XMLHttpRequest"
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

         destroy = {
             "_method": "DELETE",
             "authenticity_token": "",
             "id": ""
         }

         
         try: 
             response = session.get(self.host_url, headers=headers, allow_redirects=False)
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
             login = session.post(self.session_url, headers=headers, data=payload, allow_redirects=False)
             if login.status_code == 302 or login.status_code == 200:
                 print "[+] Loggined successfully, HTTP Status Code: %d" % login.status_code
                 headers[X-Twitter-Active-User] = "yes"
             else:
                 print "[+] Failed to loggin, HTTP Status Code: %d" % login.status_code
             
         except:
             "[+] An error occurred in the middle of the login."
             
         try:
            tweet = session.post(self.tweet_url, data=tweet, allow_redirects=False, headers=headers, cookies=login.cookies)
            if tweet.status_code == 200:
                print "[+] Tweeted successfully, HTTP Status Code: %d" % tweet.status_code
            elif tweet.status_code == 403: 
                response = session.get(self.mypage_url, headers=headers, allow_reidrects=False)
                soup = BeautifulSoup(response.text, "lxml")
                destroy['id'] = soup.find('div', attrs={'class':'stream=container'}).get('data-max-position')
                dest = session.post(self.destroy_url, data=destroy, allow_redirects=False, headers=headers, cookies=login.cookies)
                if dest.status_code == 200:
                    print "[+] Deleted the duplicate tweets successfully, HTTP Status Code: " % dest.status_code
                else:
                    print "[+] Failed to delete the duplicate tweets, HTTP Status Code: " % tweet.status_code
            else:
                print "[+] Failed to tweet, HTTP Status Code: %d" % tweet.status_code
             
         except: 
            "[+] An error occurred in the middle of tweeting."
if __name__ == "__main__":
     TwiTweet = TwitterTweet()
     TwiTweet.tweet()                
