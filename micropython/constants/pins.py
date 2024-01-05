from machine import Pin

p1 = Pin(15, Pin.IN, Pin.PULL_DOWN)  # Green LED   -- pin 20
p2 = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Blue LED    -- pin 19
p3 = Pin(13, Pin.IN, Pin.PULL_DOWN)  # Red LED     -- pin 17
p4 = Pin(12, Pin.IN, Pin.PULL_DOWN)  # Future work -- pin 16

switch = Pin(18, Pin.IN, Pin.PULL_DOWN)  # pin 24
led_1 = Pin(16, Pin.OUT)
led_2 = Pin(17, Pin.OUT)


