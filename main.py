import time
import json
from NixieDriver import NixieDriver
from machine import Pin, I2C
from ds3231 import DS3231


class Main:
    settings = None
    onboardLed = None
    nixie = []
    i2c0 = None
    i2c1 = None
    ds = None

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
            for digit in self.settings['digits']:
                address = int(digit['address'], 16)
                self.nixie.append(NixieDriver(i2c=self.i2c0,
                                              address=address,
                                              digitPins=digit['digitPins'],
                                              ncPin=digit['ncPin'],
                                              position=digit['position']))

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

    def set_date(self):
        year = 2024 # Can be yyyy or yy format
        month = 7
        mday = 28
        hour = 19 # 24 hour format only
        minute = 38
        second = 00 # Optional
        weekday = 7 # Optional
        datetime = (year, month, mday, hour, minute, second, weekday)
        self.ds.datetime(datetime)

    def set_display(self, datetime_tuple):
        # datetime_tuple format is (year, month, day, weekday, hour, minutes, seconds, 0)
        hour = datetime_tuple[4]      # hour is at index 4
        minute = datetime_tuple[5]    # minutes at index 5
        second = datetime_tuple[6]    # seconds at index 6
        
        # Convert to strings with leading zeros and get individual digits
        hour_str = f"{hour:02d}"
        minute_str = f"{minute:02d}"
        second_str = f"{second:02d}"
        
        # Create a list of all digits we want to display
        all_digits = [
            int(hour_str[0]),    # position 0
            int(hour_str[1]),    # position 1
            int(minute_str[0]),  # position 2
            int(minute_str[1]),  # position 3
            int(second_str[0]),  # position 4
            int(second_str[1])   # position 5
        ]
        
        # Set each nixie tube based on its position
        for tube in self.nixie:
            tube.set_digit(all_digits[tube.position])

    def run_clock(self):
        while True:
            curtime = self.get_datetime()
            self.set_display(curtime)
            time.sleep(0.5)

if __name__ == '__main__':
    main = Main()
    main.run_clock()
    '''
    while True:    
        
        for i in range(0, 999999):
            num_str = f"{i:06d}"
            digits = [int(d) for d in num_str]
            curtime = main.get_datetime()
            print(f"time: {curtime} digits: {digits}")
            main.nixie[0].set_digit(digits[5])
            main.nixie[1].set_digit(digits[4])
            main.nixie[2].set_digit(digits[3])
            main.nixie[3].set_digit(digits[2])
            main.nixie[4].set_digit(digits[1])
            main.nixie[5].set_digit(digits[0])
            time.sleep(1)
    '''