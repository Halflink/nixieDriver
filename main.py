import time
import json
from NixieDriver import NixieDisplay
from machine import Pin, I2C
from ds3231 import DS3231
from rotary import RotarySwitch


class Main:
    settings = None
    onboardLed = None
    nixie = []
    i2c0 = None
    i2c1 = None
    ds = None
    nixieDisplay = None
    rotary = None

    def __init__(self):
        f = open("settings.json")
        self.settings = json.load(f)
        self._validate_settings()
        self.onboardLed = Pin(self.settings['onboardLedPin'], Pin.OUT)

        rotary_settings = self.settings.get('rotary')
        if rotary_settings is not None:
            print("set rotary")
            self.rotary = RotarySwitch(
                pin_a=rotary_settings['pin_a'],
                pin_b=rotary_settings['pin_b'],
                button_pin=rotary_settings['button_pin'],
            )

        self.i2c0 = I2C(0,
                        sda=Pin(self.settings['i2c0']['sdaPin']),
                        scl=Pin(self.settings['i2c0']['sclPin']),
                        freq=100000)
        self.i2c1 = I2C(1,
                        sda=Pin(self.settings['i2c1']['sdaPin']),
                        scl=Pin(self.settings['i2c1']['sclPin']),
                        freq=100000)

        time.sleep(1)
        if self.scan_i2c(self.i2c0):
            self.nixieDisplay = NixieDisplay(i2c=self.i2c0,
                                             address=0,
                                             digits=self.settings['digits'])
            
        if self.scan_i2c(self.i2c1):
            self.ds = DS3231(self.i2c1)
            print("found second ic2")
            if self.ds.OSF():
                print("RTC oscillator stop flag set, initializing from settings.json basedate")
                self.set_date()

    def _validate_settings(self):
        required_keys = ['onboardLedPin', 'i2c0', 'i2c1', 'digits']
        missing = [key for key in required_keys if key not in self.settings]
        if missing:
            raise ValueError('Missing required setting(s): ' + ', '.join(missing))

        for bus_key in ['i2c0', 'i2c1']:
            bus = self.settings.get(bus_key)
            if not isinstance(bus, dict):
                raise ValueError('Setting ' + bus_key + ' must be an object')
            for pin_key in ['sdaPin', 'sclPin']:
                if pin_key not in bus:
                    raise ValueError('Missing required setting: ' + bus_key + '.' + pin_key)

        digits = self.settings.get('digits')
        if not isinstance(digits, list) or len(digits) == 0:
            raise ValueError('Setting digits must be a non-empty list')
        for idx, digit in enumerate(digits):
            if not isinstance(digit, dict):
                raise ValueError('digits[' + str(idx) + '] must be an object')
            for digit_key in ['position', 'address', 'digitPins', 'ncPin']:
                if digit_key not in digit:
                    raise ValueError('Missing required setting: digits[' + str(idx) + '].' + digit_key)

        basedate = self.settings.get('basedate')
        if basedate is not None:
            if not isinstance(basedate, dict):
                raise ValueError('Setting basedate must be an object')
            for date_key in ['year', 'month', 'mday', 'hour', 'minute']:
                if date_key not in basedate:
                    raise ValueError('Missing required setting: basedate.' + date_key)

        rotary_settings = self.settings.get('rotary')
        if rotary_settings is not None:
            if not isinstance(rotary_settings, dict):
                raise ValueError('Setting rotary must be an object')
            for pin_key in ['pin_a', 'pin_b', 'button_pin']:
                if pin_key not in rotary_settings:
                    raise ValueError('Missing required setting: rotary.' + pin_key)

    def get_datetime(self):
        return self.ds.datetime()

    def set_date(self):
        basedate = self.settings.get('basedate')
        if basedate is None:
            raise ValueError('Missing required setting: basedate')

        year = int(basedate['year']) # Can be yyyy or yy format
        month = int(basedate['month'])
        mday = int(basedate['mday'])
        hour = int(basedate['hour']) # 24 hour format only
        minute = int(basedate['minute'])
        second = int(basedate.get('second', 0)) # Optional
        weekday = int(basedate.get('weekday', 0)) # Optional

        datetime = (year, month, mday, hour, minute, second, weekday)
        self.ds.datetime(datetime)

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

    def set_time_mode(self):
        """Interactive time-setting using the rotary encoder.
        
        Flow: set hours (pos 0,1) -> set minutes (pos 2,3) -> set seconds (pos 4,5)
        Active pair blinks, others are dark. Rotate to change value, push to confirm.
        After seconds are confirmed, the new time is written to the RTC.
        """
        # Read current time as starting values
        curtime = self.get_datetime()
        values = [curtime[4], curtime[5], curtime[6]]  # hour, minute, second
        limits = [23, 59, 59]
        position_pairs = [{0, 1}, {2, 3}, {4, 5}]
        labels = ["hours", "minutes", "seconds"]

        for stage in range(3):
            print("Setting", labels[stage])
            self.rotary.reset_position()
            self.rotary.was_pressed()  # clear any pending press
            base_value = values[stage]
            blink_on = True
            last_toggle = time.ticks_ms()

            while True:
                # Calculate new value from rotary offset
                offset = self.rotary.get_position()
                val = (base_value + offset) % (limits[stage] + 1)
                if val < 0:
                    val += limits[stage] + 1
                values[stage] = val

                # Build the 6-digit list
                digits = [
                    values[0] // 10, values[0] % 10,
                    values[1] // 10, values[1] % 10,
                    values[2] // 10, values[2] % 10,
                ]

                # Blink the active pair (~300ms toggle)
                now = time.ticks_ms()
                if time.ticks_diff(now, last_toggle) > 300:
                    blink_on = not blink_on
                    last_toggle = now

                if blink_on:
                    self.nixieDisplay.show_digits(digits, position_pairs[stage])
                else:
                    self.nixieDisplay.all_dark()

                # Button press confirms this stage
                if self.rotary.was_pressed():
                    break

                time.sleep(0.05)

        # Write the new time to the RTC
        # Keep current date, update h/m/s
        year = curtime[0]
        month = curtime[1]
        day = curtime[2]
        weekday = curtime[3]
        new_datetime = (year, month, day, values[0], values[1], values[2], weekday)
        self.ds.datetime(new_datetime)
        print("Time set to {:02d}:{:02d}:{:02d}".format(values[0], values[1], values[2]))

    def run_clock(self):
        # Cathode cycling settings
        cycling = self.settings.get('cathodeCycling')
        if cycling:
            cycle_interval_ms = cycling['interval'] * 1000
            cycle_speed = cycling['speed']
        else:
            cycle_interval_ms = 0

        last_cycle = time.ticks_ms()

        while True:
            # Check if button was pressed to enter set-time mode
            if self.rotary is not None and self.rotary.was_pressed():
                print("rotary pressed")
                self.set_time_mode()

            # Cathode anti-poisoning cycle
            if cycle_interval_ms > 0:
                now = time.ticks_ms()
                if time.ticks_diff(now, last_cycle) >= cycle_interval_ms:
                    self.nixieDisplay.cathode_cycle(cycle_speed)
                    last_cycle = time.ticks_ms()

            curtime = self.get_datetime()
            # print(curtime)
            self.nixieDisplay.set_display(curtime)
            time.sleep(0.5)


if __name__ == '__main__':
    main = Main()
    main.run_clock()
