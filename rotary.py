from machine import Pin
import time

class RotarySwitch:
    def __init__(self, pin_a, pin_b, button_pin):
        self.pin_a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(pin_b, Pin.IN, Pin.PULL_UP)
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        
        self.last_state = self.pin_a.value()
        self.position = 0
        
        # Attach interrupts
        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.handle_rotation)
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_button)

    def handle_rotation(self, pin):
        current_state = self.pin_a.value()
        if current_state != self.last_state:
            if self.pin_b.value() != current_state:
                self.position += 1  # Clockwise
            else:
                self.position -= 1  # Counter-clockwise
            self.last_state = current_state

    def handle_button(self, pin):
        print("Button pressed!")

    def get_position(self):
        return self.position

    def reset_position(self):
        self.position = 0