try:
    import logging
except:
    import ulogging as logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('boot')

import network
import os

from config import NETWORK

# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html#configuration-of-the-wifi

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('\n\n')
    log.info('connecting to network...')
    sta_if.active(True)
    sta_if.connect(NETWORK['ssid'], NETWORK['psk'])
    while not sta_if.isconnected():
        pass
    log.info('network config: %s', sta_if.ifconfig())
