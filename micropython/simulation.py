from rp2 import asm_pio, StateMachine, PIO

# Simulation SM
@asm_pio(set_init=PIO.OUT_LOW)
def in_sig_sim():
    label("delay")
    jmp(x_dec, "delay")
    wrap_target()
    set(pins, 0)
    mov(y, isr)
    label("low")
    jmp(y_dec, "low")
    set(pins, 1)
    mov(y, isr)
    label("high")
    jmp(y_dec, "high")
    wrap()

