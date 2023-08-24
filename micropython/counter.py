from rp2 import asm_pio, StateMachine, PIO


@asm_pio(sideset_init=PIO.OUT_LOW)
def counter():
    # Set scratch register y to value 3
    set(y, 3)
    # wait for 1 (high) on pin 2.  This is the counter SM; its base
    # pin is 14, so we're waiting on pin 16 to show high.  This
    # happens when either one of the triggers detects a change on the
    # pin they're watching; they do that for two cycles.
    wait(1, pin, 2)
    # Wrap up here
    wrap_target()
    # Just a label
    label("loop")
    # Set scratch register x to value 0.  Simultaneously, set side pin
    # to 1 (high).  For the counter SM, that's pin 25 -- it's set in
    # the initialization of sm4 (sideset_base).
    set(x, 0).side(1)
    # Wait for 0 (low) on pin 2.  Again, the base pin is 14, so we're
    # waiting on pin 16 to show low.  The triggers will lower pin 16
    # after two cycles.
    wait(0, pin, 2)
    # Shift 2 bits from the pins we're watching to the Input Shift
    # Register.  This will be read later on by the interrupt handler.
    # We're reading 2 pins -- so starting at the base pin of 14, that
    # means reading the state of pins 14 & 15 & putting those in the
    # ISR.
    in_(pins, 2)
    # Push the contents of the ISR into the RX fifo as one 32-bit
    # word.  Set the ISR to all zeroes.  The RX fifo now contains the
    # state of those two pins.
    push()
    # Jump to "counter start" if x is non-zero.  Irregardlessfully,
    # decrement x.
    jmp(x_dec, "counter_start")
    # Just a label
    label("counter_start")
    # Jmp to label output if pin is 1 (high).  The pin we check is set
    # by jmp_pin (EXECCTRL_JMP_PIN in assembly).  For SM4, that's pin
    # 16.  Again: the triggers will raise pin 16 if there's been a
    # change in the pin they're watching.  If they saw a HIGH up
    # above, this time it's because they've seen the LOW coming
    # after..
    jmp(pin, "output")
    # Jump to "counter start" if x is non-zero.  Irregardlessfully,
    # decrement x.
    jmp(x_dec, "counter_start")
    # Just a label.
    label("output")
    # Move the contents of scratch register x to the ISR -- *but*,
    # invert those bits first.  As a side effect, set side pin 25 to 0.
    mov(isr, invert(x)).side(0)
    # Push the contents of the ISR into the RX fifo as one 32-bit
    # word.  Set the ISR to all zeroes.  The RX fifo now contains the
    # number of 2-cycles between the first rise & the second rise.
    push()
    # Jump to "loop" if y is non-zero.  Irregardlessfully,
    # decrement y.
    jmp(y_dec, "loop")
    # Set IRQ 0x10 and wait for it to be cleared before proceeding.
    irq(block, 0x10)
    # Set scratch register y to value 3.  As a side effet, set side
    # pin 25 to 0.
    set(y, 3).side(0)
    # Wrap back to wrap target.
    wrap()
