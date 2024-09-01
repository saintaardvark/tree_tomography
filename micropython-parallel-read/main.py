from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

from paral import clock, paral_read

MAX_PINS = 8  # offset by one because pins start at zero
JMP_PIN = Pin(8)
# We're reading in 8 bits; the TX buffer is 32 bits;
RIGHT_SHIFT = 24

FREQ = 2000  # Original
# FREQ = 100_000_000


def main():
    read_sm = StateMachine(
        0, paral_read, freq=FREQ, in_base=Pin(0), sideset_base=JMP_PIN
    )
    clock_sm = StateMachine(1, clock, freq=FREQ, jmp_pin=JMP_PIN)
    # TODO: set both active at once
    read_sm.active(1)
    clock_sm.active(1)
    last = -1
    while True:
        print("Reading r...")
        r = read_sm.get()
        print("Reading clock...")
        c = clock_sm.get()
        if last == -1:
            last = c  # Hm, this is more like "time since first high pin"

        # Currently, the frequency is 2000Hz.  In clock(), the pin is
        # checked every two instructions (the length of the
        # "WAIT_FOR_P1_HIGH" routine).  Setting aside the instructions
        # in the "PUSH" routine, that means the number we read from
        # the clock is the number of milliseconds elapsed: 2000 Hz / 2
        # = 1000 Hz, or 1 millisecond.
        rzf = "{:08b}".format(r >> RIGHT_SHIFT)

        print(f"{(last-c)=}, {rzf=}")
        # sleep(1.0)


if __name__ == "__main__":
    main()
