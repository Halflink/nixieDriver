# NIXIE  TUBE DRIVER
***
## PROJECT ##
| Project name: | Halflink/nixieDriver |
|---------------|----------------------|
| Author:       | Jeroen van Zwam      |
| Date:         | 2024-05-20           |
| Last update:  | 2024-05-20           |
| Project type: | Hardware             | 


### Executable ###
* main.py 
***

## PROJECT DESCRIPTION ##


### Scope ###
* Drive a nixie tube, make it modular
* Explanation of correct wiring
* rtc module on a pico
* use a normal raspberry pico
* use three buttons to set the time (set / nexxt digit, up and down)

### Documentation
- [Driver](https://github.com/mcauser/micropython-mcp23017) written by [Mike Causer](https://github.com/mcauser)
- MCP23017 [datasheet](https://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf)
- Raspberry PI [pinout](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf)
- [Tutorial](https://electronoobs.com/eng_arduino_tut131.php) about how to drive a nixie tube using BJT transistors

*** 
## The project ##

### Hardware ###
- [MCP23017](https://www.bitsandparts.nl/IC-MCP23017-I-O-Port-Expander-16-Bit-I2C-p113665) I/O expander I2C
- [MPSA42](https://www.vanallesenmeer.nl/MPSA42-NPN-transistor-(high-voltage)) BJT high voltage transistor


