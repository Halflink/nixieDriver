from machine import Pin, I2C
import time

import mcp23017

mcp23017

onboardLed = Pin(25, Pin.OUT)

def blinkOnboardLed(nr, sleepNr):
    onboardLed.off()
    for i in range(nr*2):
        time.sleep(sleepNr)
        onboardLed.toggle()

def checkI2C():
    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
        blinkOnboardLed(5, 0.1)
        return False
    else:
        print('i2c devices found:', len(devices))
        blinkOnboardLed(3, 0.5)

    for device in devices:
        print("Decimal address: ", device, " | Hexa address: ", hex(device))

    return True

def enableLed(pin):
    mcp.pin(pin = pin, mode=0, value=1)

def disableLed(pin):
    mcp.pin(pin=pin, mode=0, value=0)

def blinkLed(pin):
    enableLed(pin)
    time.sleep(0.5)
    disableLed(pin)
    time.sleep(0.5)


onboardLed.off()

sda=machine.Pin(16) #12 / 16
scl=machine.Pin(17) #13 / 17
i2c = I2C(0, sda=sda, scl=scl, freq=400000)
time.sleep(1)

if checkI2C():
    mcp = mcp23017.MCP23017(i2c, 0x27)

if __name__ == '__main__':

    while True:
        if checkI2C():
            blinkLed(0)
            blinkLed(1)
            blinkLed(2)
            blinkLed(3)
            blinkLed(4)
            blinkLed(5)
            blinkLed(6)
            blinkLed(7)
            blinkLed(8)
            blinkLed(9)
            blinkLed(10)
            





