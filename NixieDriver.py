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
        if self.currentNumber >= 0:
            self.mcp.pin(pin=self.digitPins[self.currentNumber], mode=0, value=0)
            time.sleep(1)
        self.mcp.pin(pin=self.digitPins[nr], mode=0, value=1)
        self.currentNumber = nr
        time.sleep(1)

    def set_point_off(self):
        self.mcp.pin(pin=self.ncPin, mode=0, value=0)

    def set_point_on(self):
        self.mcp.pin(pin=self.ncPin, mode=0, value=1)


