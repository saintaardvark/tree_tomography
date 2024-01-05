# Source: https://forums.raspberrypi.com/viewtopic.php?t=306064&sid=05eb8eb20a34f7d5a7eac4cec91a7999#p1831725

""" this is a program to read the delay between 2 pins to go lo
Daniel Perron March 2021"""

import utime
import rp2
from rp2 import PIO, asm_pio
from machine import Pin

"""
pin 1 _______              _________
             \____________/

pin2 ____________        ________
                 \______/
             
       A   B  C   D
  
  
  A= be sure that pin2 is high
  B= be sure that pin1 is high
  C= detect pin 1 is low (dec X)
  D= detect pin 2 is low
"""


@asm_pio()
def PULSE_LOW_DELTA():
    # clock set at 100MHz

    # Initialize x to be -1
    set(x, 0)
    jmp(x_dec, "WAIT_FOR_P1_HIGH")

    # Wait for pin1 to be high
    label("WAIT_FOR_P1_HIGH")
    wait(1, pin, 0)

    # ok, pin 1 is up; now just dec x until pin2 is high
    label("WAIT_FOR_P2_HIGH")
    # If pin -- the jmp_pin, which is the p2 arg to pulsedelay() -- is
    # high, then jump to "loopExit"
    jmp(pin, "loopExit")
    # Jump to "loopCount" if x is non-zero.  It is -- we set it at the
    # top.  Irregardlessfully, decrement x.  This is basically a way
    # to decrement x every time we go through this particular loop.
    jmp(x_dec, "WAIT_FOR_P2_HIGH")

    # ok we got Pin 2 low! register it by push
    label("loopExit")
    mov(isr, x)
    push()
    label("End")
    jmp("End")


class pulsedelay:
    def __init__(self, pin1, pin2, stateMachine=0):
        self.pin1 = pin1
        self.pin2 = pin2
        self.sm = rp2.StateMachine(stateMachine)

    def activate(self):
        self.sm.init(
            PULSE_LOW_DELTA, freq=100_000_000, in_base=(self.pin1), jmp_pin=(self.pin2)
        )
        self.sm.active(1)

    def get(self):
        """ in_base declare the first Pin offset
            jmp_pin declare the pin to use for jmp (this is not an offset)
        """
        # adjust for microsecond value
        # - 100 MHz == 10 nanoseconds per clock cycle
        # - there are two instructions in the close loop
        # - 20 nanoseconds per loop
        # - 1000 nanoseconds = 1 microsecond
        # - therefore, divide by 50
        return (0xFFFFFFFF - self.sm.get()) / 50


# if __name__ == "__main__":
#     from machine import Pin
#     from pulsedelay import pulsedelay
#     import utime

#     p1 = Pin(16,Pin.IN)
#     p2 = Pin(17,Pin.IN)
#     pulsein = pulsedelay(p1,p2)

#     while True:
#         print(pulsein.get())
