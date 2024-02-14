try:
    import logging
except:
    import ulogging as logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('main')

from uflask import Flask
from remote import Remote
from components import Components

from usb_switch import UsbSwitch

try:
    import network

    def my_ip():
        return network.WLAN(network.STA_IF).ifconfig()[0]
except:
    import socket

    def my_ip():
        return socket.gethostbyname(socket.gethostname())


app = Flask()
remote = Remote()
usb_switch = UsbSwitch(25, 26)
usb_switch.enable()

components = Components()

@app.route("^\/$")
def index(match):
    from index_html_tpl import render
    return render(components, my_ip())


@app.route("^\/style.css$")
def index(match):
    from style_css_tpl import render
    return render()


@app.route("^\/ir\?cmd=(.*)$")
def ir(match):
    cmd = int(match.group(1), 16)
    remote.send_command(cmd, 0x01)


@app.route("^\/usb\?select=(.*)$")
def usb(match):
    value = int(match.group(1))
    usb_switch.select(value)


app.run_forever()
