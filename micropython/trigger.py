from rp2 import asm_pio, StateMachine, PIO


@asm_pio(set_init=PIO.OUT_HIGH)
def trigger():
    # Wait for 1 (high) on pin 0.  For SM2, that's Pin 14.  For SM3,
    # that's Pin 15.
    wait(1, pin, 0)
    # Set pins to 1 (high) & do this for 2 add'l cycles.  For both state
    # machines, that's Pin 16.
    set(pins, 1)[2]
    # Set pins to 0 (low).  Again, Pin 16.
    set(pins, 0)
    # Wait for 0 (low) on pin 0.  For SM2, that's Pin 14.  For SM3,
    # that's Pin 15.
    wait(0, pin, 0)
    # Set pins to 1 (high) & do this for 2 add'l cycles.  For both state
    # machines, that's Pin 16.
    set(pins, 1)[2]
    # Set pins to 0.
    set(pins, 0)
