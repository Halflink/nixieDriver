from machine import Pin
import time

class RotarySwitch:
    def __init__(self, pin_a, pin_b, button_pin, steps_per_click=2):
        self.pin_a = Pin(pin_a, Pin.IN)
        self.pin_b = Pin(pin_b, Pin.IN)
        self.button = Pin(button_pin, Pin.IN)
        
        self.last_state = self.pin_a.value()
        self.position = 0
        self.steps_per_click = steps_per_click
        self.button_pressed = False
        self._last_button_time = 0
        
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
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_button_time) > 250:
            self.button_pressed = True
            self._last_button_time = now

    def was_pressed(self):
        """Check if button was pressed since last check, and clear the flag."""
        if self.button_pressed:
            self.button_pressed = False
            return True
        return False

    def get_position(self):
        return self.position // self.steps_per_click

    def reset_position(self):
        self.position = 0