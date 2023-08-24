# Source: https://forums.raspberrypi.com/viewtopic.php?t=306064&sid=f40cf17605a796b93c59b94721dd322b#p1842706
#
# This is a little bit different from main.py:
#
# - this post comes from the thread & the original author, whereas
#   main.py comes from J. Beale's github repo.
#
# - But also, this code was corrected by the original author (set vs
#   mov), and those changes don't seem to have been captured in the
#   github repo.
#
# - finally, the simulated signals are in here too.

from machine import Pin, mem32
from rp2 import asm_pio, StateMachine, PIO
from time import ticks_ms, ticks_diff
from utime import sleep
import array

from my_mpu import MyMpu
from simulation import in_sig_sim, start_sig_sim
from trigger import trigger
from counter import counter


data = array.array("I", [0] * 8)
start = ticks_ms()
# This comes from the self-test part of the mput driver.  These are
# probably bogus values; this was done with the sensor at a random
# angle.  However, it doesn't seem to hurt it when doing early testing
# to detect motion.
OFS = (878, -1385, 1560, 136, -54, -16)

START_SIG_SIM = False
EVENTS = []

def mpu_handler(data: tuple):
    if "mpu" in globals():
        print("[{:<16}] {:<10.2f}".format("TEMPERATURE", mpu.celsius))
        mpu.print_from_data(data)


def counter_handler(sm):
    global start, EVENTS
    for i in range(8):
        data[i] = sm.get()
    print(ticks_diff(ticks_ms(), start), data)
    # FIXME: I should be using a mutex here: https://docs.openmv.io/library/mutex.html
    EVENTS.append(data)
    start = ticks_ms()


if START_SIG_SIM is True:
    start_sig_sim()

# TODO: Haven't tried to set the clock faster, but probably should --
# I think the motion threshold time right now is ~ 1 ms, which is
# rather slow.
# TODO: We're setting the handler here for debugging.  This depends on
# having the MPU interrupt pin connected to both GPIO 2 *and* 14.
# At some point, we'll want to stop that.

mpu = MyMpu(bus=0, sda=20, scl=21, ofs=OFS, intr=2, callback=mpu_handler)
if mpu.passed_self_test:
    print("Ready to set up mpu!")
    mpu.start()

sm2 = StateMachine(2, trigger, freq=100_000_000, in_base=Pin(14), set_base=Pin(16))
sm2.active(1)
sm3 = StateMachine(3, trigger, freq=100_000_000, in_base=Pin(15), set_base=Pin(16))
sm3.active(1)

sm4 = StateMachine(
    4, counter, freq=100_000_000, in_base=Pin(14), jmp_pin=Pin(16), sideset_base=Pin(25)
)
sm4.irq(counter_handler)

PIO0_BASE = 0x50200000
PIO1_BASE = 0x50300000
PIO_CTRL = 0x000
SM0_EXECCTRL = 0x0CC
SM0_SHIFTCTRL = 0x0D0
# Join output FIFOs for sm4
mem32[PIO1_BASE | SM0_SHIFTCTRL + 0x1000] = 1 << 31
sm4.active(1)
# Start sm0 and sm1 in sync
mem32[PIO0_BASE | PIO_CTRL + 0x1000] = 0b11

while True:
    try:
        # FIXME: Again, should be using a mutex
        d = EVENTS.pop()
        print(d)
    except IndexError:
        print("No news...")
    mpu.reset_interrupt()
    sleep(1)
