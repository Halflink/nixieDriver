import time
import json
from NixieDriver import NixieDriver
from machine import Pin, I2C

class Main:

    settings = None
    onboardLed = None
    nixie = []
    i2c = None

    def __init__(self):
        f = open("settings.json")
        self.settings = json.load(f)
        self.onboardLed = Pin(self.settings['onboardLedPin'], Pin.OUT)
        self.i2c = I2C(0,
                       sda=self.settings['sdaPin'],
                       scl=self.settings['sclPin'],
                       freq=40000)
        time.sleep(1)
        if self.scan_i2c():
            for digit in self.settings['digits']:
                address = int(digit['address'], 16)
                self.nixie.append(NixieDriver(i2c=self.i2c,
                                              address=address,
                                              digitPins=digit['digitPins'],
                                              ncPin=digit['ncPin'],
                                              position=digit['position']))

    def blink_onboard_led(self, nrOfBlinks, sleepNr):
        self.onboardLed.off()
        for i in range(nrOfBlinks*2):
            time.sleep(sleepNr)
            self.onboardLed.toggle()

    def scan_i2c(self):
        print('Scan i2c bus...')
        devices = self.i2c.scan()

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


if __name__ == '__main__':

    main = Main()
    while True:
        for i in range(0, 99999):
            num_str = f"{i:05d}"
            digits = [int(d) for d in num_str]
            print(digits)
            main.nixie[0].set_digit(digits[4])
            main.nixie[1].set_digit(digits[3])
            main.nixie[2].set_digit(digits[2])
            main.nixie[3].set_digit(digits[1])
            main.nixie[4].set_digit(digits[0])
            time.sleep(1)

