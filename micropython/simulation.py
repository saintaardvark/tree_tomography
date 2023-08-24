from machine import Pin
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


def start_sig_sim():
    """
    Instantiate and configure signal simulating SMs
    """
    sm0 = StateMachine(0, in_sig_sim, freq=1_000_000, set_base=Pin(14))
    sm0.put(500_000) # Frequency control
    sm0.exec("pull()")
    sm0.exec("mov(isr, osr)")
    sm0.put(100_000) # Delay control
    sm0.exec("pull()")
    sm0.exec("mov(x, osr)")
    sm1 = StateMachine(1, in_sig_sim, freq=1_000_000, set_base=Pin(15))
    sm1.put(500_000) # Frequency control
    sm1.exec("pull()")
    sm1.exec("mov(isr, osr)")
    sm1.put(1) # Delay control
    sm1.exec("pull()")
    sm1.exec("mov(x, osr)")

