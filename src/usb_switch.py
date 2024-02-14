try:
    from machine import Pin


    class UsbSwitch:
        def __init__(self, oe_pin, s_pin):
            self.oe_pin = Pin(oe_pin)
            self.s_pin = Pin(s_pin)
            self.oe_pin.init(mode=Pin.OUT, pull=None, value=1)
            self.s_pin.init(mode=Pin.OUT, pull=None, value=1)

        def enable(self):
            self.oe_pin.value(0)

        def disable(self):
            self.oe_pin.value(1)

        def select(self, value):
            self.s_pin.value(value)
except:
    class UsbSwitch:
        def __init__(self, oe_pin, s_pin):
            pass

        def enable(self):
            pass

        def disable(self):
            pass

        def select(self, value):
            pass
