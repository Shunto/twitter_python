# -*- coding: utf-8 -*-
# user_id.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import sys

class TwitterUserID:
    def __init__(self):
        self.user_id = ""
        
    def userid(self):
        session = requests.Session()
        headers = {                                                                      
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
            "Referer": "https://twitter.com/",
            "Origin": "https://twitter.com",
            "Upgrade-insecure-requests": "1"
        }
        
        try:
            url = "https://twitter.com/" + raw_input("The user whose user_id you want to know: ")
            response = session.get(url, headers=headers, allow_redirects=False)
            soup = BeautifulSoup(response.text, "lxml")
            self.user_id = soup.find('div', attrs={'class':'ProfileNav'}).get('data-user-id')
        except:
            "[+] A connection error occurred while tweeting"
        return self.user_id

if __name__ == "__main__":
    TwiUserid = TwitterUserID()
    print "[+] The user_id of the user: " + TwiUserid.userid()
