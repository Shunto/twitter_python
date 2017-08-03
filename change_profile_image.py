# -*- coding: utf-8 -*-
# change_profile_image.py
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import json
import os

SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
PATH = "./images/IMG_0005.PNG"

USERNAME = "ShuntoMizushima"
PASSWORD = "mizushima4105"

def changeimage():
    global SESSION, RESPONSE, AUTH_TOKEN

    login = {                           
        "session[username_or_email]":USERNAME,
        "sesssion[password]":PASSWORD,
        "remember_me": "1",
        "return_to_ssl": "",
        "redirect_after_login": "/",
        "scribe_log": ""
    }
    
    image = {
        "authenticity_token":"",
        "height":"512",
        "mediaId":"",
        "offsetLeft":"0",
        "offsetTop":"0",
        "page_context":"upload",
        "section_context":"profile",
        "uploadType":"avatar",
        "width":"512"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://twitter.com/",
        "Origin": "https://twitter.com",
        "Upgrade-Insecure-Requests": "1",
        "X-Requested-With":"smLHttpRequest"
    }
    
    imageheaders = {
        "User-Agent":"Mozilla/5.0",
        "Accept":"*/*", 
        "Accept-Language": "gzip, deflate, br",
        "Referer": "https://twitter.com/",
        "Origin": "https://twitter.com",
        "Authority":"upload.twitter.com",
        "Content-Length":"117291"
    }
    
    try:
        RESPONSE = SESSION.get('https://twitter.com/', headers=headers, allow_redirects=False)
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        AUTH_TOKEN = soup.find(attrs={'name':'authenticity_token'}).get('value')
        login['authenticity_token'] = AUTH_TOKEN
        image['authenticity_token'] = AUTH_TOKEN
        RESPONSE = SESSION.post('https://twitter.com/sessions', data=login, allow_redirects=False, headers=headers)
    except Exception as e:
        print "[+] Failed to login."

    imageids = SESSION.post("https://upload.twitter.com/i/media/upload.json?command=INIT&total_bytes=" + str(os.path.getsize(PATH)) + "&media_type=image%2Fpng&media_category=tweet_image", headers=headers, cookies=RESPONSE.cookies)

    imageids = imageids.json()
    imageid = imageids['media_id']
    image['mediaId'] = imageid
    files = {'media':open(PATH, 'rb')}

    RESPONES = SESSION.post("https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id=" + str(imageid) + "&segment_index=0", files=files, headers=imageheaders, cookie=RESPONSE.cookies)

    RESPONSE = SESSION.post("https://twitter.com/i/profiles/updata_profile_image", data=image, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)

    print "[+] Updated your profile, HTTP Status Code: %d" % RESPONSE.status_code
    print RESPONSE.text


if __name__ == "__main__":
    changeimage()
