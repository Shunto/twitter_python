#-*- coding: utf-8 -*-
# create_tweet_account.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from json import load
import socket, socks, requests
import random, sys, csv, time
import string

class TwitterCreateAccount:
     def __init__(self):
         ip = 'localhost'
         port = 9050
         socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
         socket.socket = socks.socksocket
         self.screenname = ""
         self.host_url = "https://twitter.com/"
         self.mypage_url = self.host_url + self.username
         self.session_url = self.host_url + "sessions"
         self.new_account_url = self.host_url + "account/create"
         self.tweet_url = self.host_url + "i/tweet/create" 
         self.destroy_url = self.host_url + "i/tweet/destroy"
         self.retweet_url = self.host_url + "i/tweet/retweet"
         self.follow_url = self.host_url + "i/user/follow"
         self.like_url = self.host_url + "i/tweet/like"
     
     
     def getScreenName(self):
         return self.screenname
        
     def mail(self):
         string_letters = string.letters
         source_str = string_letters + "1234567890" 
         username = "r00t" + "".join([random.choice(source_str) for x in xrange(8)])
         domain = "root" + "".join([random.choice(source_str) for x in xrange(8)])
         mail = username + "@" + domain + ".com"
         self.screenname = username
         return mail
      
     def main(self):
         payload = {
             "authenticity_token": "",
             "signup_ui_metrics": "",
             "m_metrics": "",
             "d_metrics": "",
             "user[name]": "",
             "user[email]": "",
             "user[user_password]": "Passw0rd",
             "user[use_cookie_personalization]": "1",
             "asked_cookie_personalization_setting": "1",
             "ad_ref": "",
             "user[discoverable_by_email]": "1",
             "asked_discoverable_by_email": "1",
             "user[discoverable_by_mobile_phone]": "1",
             "asked_discoverable_by_mobile_phone": "1"
             
         }
         tweet = {                          
             "authenticity_token": "",     
             "is_permalink_page": "false",
             "place_id": "",
             "status": "test",
             "tagged_users": ""
         }

         follow = {
             "authenticity_token": "",
             "challenges_passed": "false",
             "handles_challenge": "1",
             "user_id": ""
         }

         fav = {
             "authenticity_token": "",
             "id": "",
             "tweet_stat_count": "0"
         }    
         
         retweet = {
             "authenticity_token": "",
             "id": "",
             "tweet_stat_count": "0"
         }

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
         try: 
             response = session.get(self.host_url, headers=headers, allow_redirects=False)
             soup = BeautifulSoup(response.text, "lxml")
             auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
         except ConnectionError:
             print "[*] Can't connect to Twitter."
             sys.exit()
                                                                                                                                   
                                                                                              try:
             try:
                 payload['authenticity_token'] = auth_token
                 payload['user[email]'] = self.mail()
                 payload['user[name]'] = self.getScreenName()
                 response = session.post(self.new_account_url, data=payload, allow_redirects=False, headers=headers)
                 print "[*] Created a new account, HTTP Status Code: %d" % response.status_code
             except:
                 print "[+] Failed to create a new account."

             try:
                 print "==================================="
                 twitter_username = payload['user[name]']
                 url = self.host_url + twitter_username
                 print "[+] Authenticity token.....: %s" % payload['authenticity_token']
                 print "[+] Timeline URL.....: %s" % url
                 print "[+] Username.....: %s" % payload['user[name]']
                 print "[+] Account mail address.....: %s" % payload['user[email]']
                 print "[+] Account password.....: %s" % payload['user[user_password]']
                 print "==================================="
             except:
                 print "[+] An error occurred while showing the result although account had been created successfully."
         except ConnectionError:
             print "[+] Exit because the connection is unstable."
             sys.exit() 
        
         if response.status_code == 302:
             try:
                 try:
                     response = session.get(url, headers=headers, allow_redirects=False)
                     print "[+] Connect to " + url + ", HTTP Status Code: %d" % response.status_code
                 except:
                     print "[+] Can't connect to %s" % url
                     
                 if response.status_code != 200:
                     print "[+] You need to authentite your account with your phone number."
                     sys.exit()
                 elif response.status_code == 200:
                     print "[+] The account was created without any problem." 

                     try:
                         follow['authenticity_token'] = auth_token
                         tweet['authenticity_token'] = auth_token
                         retweet['authenticity_token'] = auth_token

                         response = session.post(self.follow_url, data=follow, allow_redirets=False, headers=headers, cookies=response.cookies)
                         print "[+] Completed following, HTTP Status Code: %d" % response.status_code
                         
                         response = session.post(self.tweet_url, data=tweet, allow_redirects=False, headers=headers, cookies=response.cookies)
                         print "[+] Completed a tweet, HTTP Status Code: %d" % response.status_code
                         
                         response = session.post(self.like_url, data=fav, allow_redirects=False, headers=headers, cookies=response.cookies)
                         print "[+] Completed liking, HTTP Status Code: %d" % response.status_code
                         
                         response = session.post(self.retweet_url, data=retweet, allow_redirects=False, headers=headers, cookies=response.cookies)
                         print "[+] Completed a retweet, HTTP Status Code: %d" % response.status_code
                     except:
                         print "[+] Failed to follow"
                     finally:
                         sys.exit()
             except ConnectionError:
                 print "[+] Connection error: %s" % url                                               sys.exit()                                          
             finally:
                 return 
         else:
             print "[+] HTTP Status Code: %d" % response.status_code
if __name__ == "__main__":
    TwiACC = TwitterCreateAccount()
    start = time.time()
    TwiACC.main()
    elapsed_time = time.time() - start
    print ("[*] Total processing time is {0}".format(elapsed_time)) + "[seconds(Currently interval that ip is changed with Tor is 20 seconds]]\n"
