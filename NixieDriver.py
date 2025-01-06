import mcp23017
import time


class NixieDriver:

    digitPins = []
    currentNumber = -1

    def __init__(self, i2c, address, digitPins, ncPin, position):
        self.mcp = mcp23017.MCP23017(i2c, address)
        self.digitPins = digitPins
        self.ncPin = ncPin
        self.position = position

    def set_digit(self, nr):
        if nr != self.currentNumber:
            if self.currentNumber >= 0:
                self.mcp.pin(pin=self.digitPins[self.currentNumber], mode=0, value=0)
            self.mcp.pin(pin=self.digitPins[nr], mode=0, value=1)
            self.currentNumber = nr

    def set_point_off(self):
        self.mcp.pin(pin=self.ncPin, mode=0, value=0)

    def set_point_on(self):
        self.mcp.pin(pin=self.ncPin, mode=0, value=1)


class NixieDisplay:

    nixie_display = []

    def __init__(self, i2c, address, digits):
        for digit in digits:
                address = int(digit['address'], 16)
                self.nixie_display.append(NixieDriver(i2c=i2c,
                                                      address=address,
                                                      digitPins=digit['digitPins'],
                                                      ncPin=digit['ncPin'],
                                                      position=digit['position']))

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
        for tube in self.nixie_display:
            tube.set_digit(all_digits[tube.position])
