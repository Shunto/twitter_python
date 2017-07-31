# -*- coding: utf-8 -*-
# ip.py
import socket, socks, requests
import requests

class Tor:
    def __init__(self):
        ip='localhost'
        port = 9050
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
        socket.socket = socks.socksocket

    def get_ip(self):
        session = requests.Session()
        try:
            ip_addr = session.get('https://api.ipify.org/').text
            return ip_addr
        except socks.ProxyConnectionError:
            print "[+] Proxy Error"

        return 

if __name__ == "__main__":
    Tor = Tor()
    ip = Tor.get_ip()
    print ip
