try:
    import logging
except:
    import ulogging as logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('main')

try:
    import esp32
    from machine import Pin


    class Remote:
        def __init__(self):
            self.rmt = esp32.RMT(0, pin=Pin(2), clock_div=8, tx_carrier=(40000, 50, 1))
            log.info(f"RMT source_freq: {self.rmt.source_freq()}")
            log.info(f"RMT clock_div: {self.rmt.clock_div()}")
            resolution_us = 1000000 / (self.rmt.source_freq() / self.rmt.clock_div())
            log.info(f"resolution_us: {resolution_us}")
            self.HEADER = [int(2400/resolution_us), int(600/resolution_us)]
            self.BIT = [[int(600/resolution_us), int(600/resolution_us)], [int(1200/resolution_us), int(600/resolution_us)]]

        def send_command(self, command, address):
            log.info(f"command {command} address {address}")
            msg = [] + self.HEADER
            for i in range(7):
                msg += self.BIT[(command >> i) & 1]
            for i in range(5):
                msg += self.BIT[(address >> i) & 1]
            self.rmt.write_pulses(msg, 1)
except:
    class Remote:
        def send_command(self, command, address):
            log.info(f"command {command} address {address}")
