# -*- coding: utf-8 -*-
#auth2.py
from bs4 import BeautifulSoup
import requests

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": "https://twitter.com/",
    "Origin": "https://twitter.com",
    "Upgrade-insecure-requests": "1"
}

response = session.get('https://twitter.com/', headers=headers, allow_redirects=False)
soup = BeautifulSoup(response.text, "lxml")
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')

print "authenticity_token: " + auth_token
print "HTTP Status code: %d" % response.status_code


