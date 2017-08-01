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
             "signup_ui_metrics": "%7B%22rf%22%3A%7B%22a772da599904e1f214aebae3b4df4491fbd2795bf2772b4ab4b051bca16db2ea%22%3A-96%2C%22e105b3c2f865ffbd694b5a6c49426276915f801a2210a32ab9a2bbce25fa64a8%22%3A-2%2C%22adf6fc7122825120a6db4b49193b4317fb09b4b45be2d9ba6f069c439c738baa%22%3A95%2C%22a1cc43395bc41fc375fad62b3460684c48d8bd84096b595667acea68516b8a6f%22%3A255%7D%2C%22s%22%3A%22vY7g7X9vOZuynhJzpLZBpOeabwlA8308dzOxXY-XWdr0r8Ju2nmdh41CE-mht2D93BBXCl2O5NVgZqfwD6suzr_fbrQ7y3ByNXU9W7sXOXvzHKJiaikwsyqEkMzY-bLcHIsYp2I_hDjUibi8eCB36lWgv8tAB27ZK4Ib5nkYzK5_CMERhW_ThPuton6Rcb8vHEKIOiewpm_girjWm2cRgiwjKj0wVe6P67wZ_cjLtWy1u7HciSSLpHiXMc8Qcy_dEPZN8c0aJSp712QEjgihVjxFj77fn7AVV7zyXHbUlyAMe6tJqaMOa2fB_5EZoc7wdK2rDcJ8VOBzmEwDQjQAuAAAAV2cY9lQ%22%7D",
             "m_metrics": "zRG4GCMAuTkAzRHQGBgAwDkAxBHnGBgAyDkAxBHzGAwA0DkAxBH%2FGAwA2DkAxBELGQwA4DkAxBEXGQwA6TkAxBEXGQAA8DkAxBEXGQAA%2BDkAxBEiGQsAADoAxBEiGQAACToAxBEiGQAADzoAxBEuGQwAGjoAvBE6GQ4AIDoAvBE6GQAAKjoAvBFGGQwAMDoAvBFGGQAAOzoAtBFSGQ4AQDoArBFpGRgATDoApBGZGTAAUToA%3APA8SC9QS3QYAsA4dDgwAOxoAbw7hEwAAUSoAXg56FFARgzgA",
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
             "user_id": "796359178117750785"
         }

         fav = {
             "authenticity_token": "",
             "id": "892264734300360706",
             "tweet_stat_count": "0"
         }    
         
         retweet = {
             "authenticity_token": "",
             "id": "892264734300360706",
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
                 print "[+] Connection error: %s" % url
                 sys.exit()                                          
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
