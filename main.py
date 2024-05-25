from machine import Pin, I2C
import time

onboardLed = Pin(25, Pin.OUT)

def blinkOnboardLed(nr, sleepNr):
    onboardLed.off()
    for i in range(nr*2):
        time.sleep(sleepNr)
        onboardLed.toggle()


onboardLed.off()

sda=machine.Pin(16) #12 / 16
scl=machine.Pin(17) #13 / 17
i2c = I2C(0, sda=sda, scl=scl, freq=400000)
time.sleep(1)



if __name__ == '__main__':

    while True:
        print('Scan i2c bus...')
        devices = i2c.scan()

        if len(devices) == 0:
            print("No i2c device !")
            blinkOnboardLed(5, 0.1)
        else:
            print('i2c devices found:',len(devices))
            blinkOnboardLed(3, 0.5)

        for device in devices:
            print("Decimal address: ",device," | Hexa address: ",hex(device))
        time.sleep(1)        
        


