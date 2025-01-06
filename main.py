import time
import json
from NixieDriver import NixieDisplay
from machine import Pin, I2C
from ds3231 import DS3231


class Main:
    settings = None
    onboardLed = None
    nixie = []
    i2c0 = None
    i2c1 = None
    ds = None
    nixieDisplay = None

    def __init__(self):
        f = open("settings.json")
        self.settings = json.load(f)
        self.onboardLed = Pin(self.settings['onboardLedPin'], Pin.OUT)
        self.i2c0 = I2C(0,
                        sda=self.settings['i2c0']['sdaPin'],
                        scl=self.settings['i2c0']['sclPin'],
                        freq=40000)
        self.i2c1 = I2C(1,
                        sda=self.settings['i2c1']['sdaPin'],
                        scl=self.settings['i2c1']['sclPin'],
                        freq=40000)

        time.sleep(1)
        if self.scan_i2c(self.i2c0):
            self.nixieDisplay = NixieDisplay(i2c=self.i2c0,
                                             address=int(self.settings['display']['address'], 16),
                                             digits=self.settings['display']['digits'])
            
        if self.scan_i2c(self.i2c1):
            self.ds = DS3231(self.i2c1)
            print("found second ic2")

    def get_datetime(self):
        return self.ds.datetime()

    def blink_onboard_led(self, nrOfBlinks, sleepNr):
        self.onboardLed.off()
        for i in range(nrOfBlinks * 2):
            time.sleep(sleepNr)
            self.onboardLed.toggle()

    def scan_i2c(self, ic2):
        print('Scan i2c bus...')
        devices = ic2.scan()

        if len(devices) == 0:
            print("No i2c device !")
            self.blink_onboard_led(10, 0.1)
            return False
        else:
            print('i2c devices found:', len(devices))
            self.blink_onboard_led(3, 0.5)

            for device in devices:
                print("Decimal address: ", device, " | Hexa address: ", hex(device))

            return True

    def run_clock(self):
        while True:
            curtime = self.get_datetime()
            self.nixieDisplay.set_display(curtime)
            time.sleep(0.5)

if __name__ == '__main__':
    main = Main()
    main.run_clock()
