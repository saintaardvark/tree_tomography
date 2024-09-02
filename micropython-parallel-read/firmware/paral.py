from rp2 import PIO, StateMachine, asm_pio


@asm_pio(
    # https://docs.micropython.org/en/v1.17/library/rp2.html: if more
    # than one pin is used in the program, out_init() needs to be a
    # tuple.  That explains the requirement of a comma for this to
    # work; I presume that the single element in the tuple means "they
    # should all be like this".
    out_init=(PIO.OUT_HIGH,) * 8,
    in_shiftdir=PIO.SHIFT_RIGHT,
    autopush=True,
    push_thresh=32,
)
def clock():
    set(x, 0)  # Set x to 0
    label("WAIT_FOR_P1_HIGH")  # Label for waiting loop
    # Wait for pin1 to be high
    jmp(pin, "PUSH")  # if pin1 is high, jump to PUSH loop.
    jmp(x_dec, "WAIT_FOR_P1_HIGH")  # Otherwise, decrement x & go to top of waiting loop
    label("PUSH")  # Beginning of PUSH loop
    in_(x, 32)  # Move 32 bits of x into [ISR?]
    jmp(x_dec, "WAIT_FOR_P1_HIGH")  # dec x & go to top of waiting loop


@asm_pio(
    set_init=PIO.OUT_LOW,
    in_shiftdir=PIO.SHIFT_RIGHT,
    sideset_init=PIO.OUT_LOW,
    autopush=True,
    push_thresh=8,
)
def paral_read():
    """
    Read in parallel
    """
    mov(y, pins)  # Move current state of pins into y
    label("main_loop")  # Beginning of main loop
    mov(x, pins)  # Move current state of pins into x
    jmp(x_not_y, "move_out")  # If x !=y, jump to move out
    jmp("main_loop")  # Otherwise, go back to reading pins
    label("move_out")  # Beginning of move_out loop
    in_(x, 8).side(1)  # Move 8 bits of x into [ISR?]; side effect: set JMP_PIN to 1
    push().side(0)  # Push out ISR; side effect: set JMP_PIN to 0
    mov(y, x)  # Move x to y
    jmp("main_loop")  # Go back to main loop
